#!/usr/bin/env python3
"""Deploy a local TMDL semantic model to a Microsoft Fabric workspace."""

from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


FABRIC_API = "https://api.fabric.microsoft.com/v1"
FABRIC_RESOURCE = "https://api.fabric.microsoft.com"
DEFAULT_MODEL_DIR = Path(__file__).resolve().parents[1] / "Contoso-DT-Dashboard.SemanticModel"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deploy the bundled TMDL semantic model through the Fabric REST API."
    )
    parser.add_argument("--workspace-id", help="Target Fabric workspace GUID.")
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=DEFAULT_MODEL_DIR,
        help=f"SemanticModel folder (default: {DEFAULT_MODEL_DIR}).",
    )
    parser.add_argument(
        "--display-name",
        default="Contoso DT Dashboard",
        help="Display name for the Fabric semantic model.",
    )
    parser.add_argument(
        "--update-existing",
        action="store_true",
        help="Replace the definition when an item with the same display name exists.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and list definition parts without authenticating or deploying.",
    )
    return parser.parse_args()


def definition_paths(model_dir: Path) -> list[Path]:
    required = [
        model_dir / "definition.pbism",
        model_dir / "definition" / "database.tmdl",
        model_dir / "definition" / "model.tmdl",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    tables_dir = model_dir / "definition" / "tables"
    table_paths = sorted(tables_dir.glob("*.tmdl")) if tables_dir.is_dir() else []

    if missing:
        raise ValueError(f"Missing required definition files: {', '.join(missing)}")
    if not table_paths:
        raise ValueError(f"No table definitions found under {tables_dir}")

    optional_paths = sorted(
        path
        for path in (model_dir / "definition").rglob("*.tmdl")
        if path not in required and path not in table_paths
    )
    return required + optional_paths + table_paths


def build_parts(model_dir: Path) -> list[dict[str, str]]:
    parts = []
    for path in definition_paths(model_dir):
        relative_path = path.relative_to(model_dir).as_posix()
        payload = base64.b64encode(path.read_bytes()).decode("ascii")
        parts.append(
            {
                "path": relative_path,
                "payload": payload,
                "payloadType": "InlineBase64",
            }
        )
    return parts


def get_access_token() -> str:
    try:
        result = subprocess.run(
            [
                "az",
                "account",
                "get-access-token",
                "--resource",
                FABRIC_RESOURCE,
                "--query",
                "accessToken",
                "--output",
                "tsv",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as error:
        raise RuntimeError("Azure CLI was not found. Install it and run 'az login'.") from error
    except subprocess.CalledProcessError as error:
        detail = error.stderr.strip() or error.stdout.strip()
        raise RuntimeError(f"Azure CLI authentication failed: {detail}") from error

    token = result.stdout.strip()
    if not token:
        raise RuntimeError("Azure CLI returned an empty Fabric access token. Run 'az login'.")
    return token


def request_json(
    method: str,
    url: str,
    token: str,
    body: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any], dict[str, str]]:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urlopen(request, timeout=60) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw) if raw else {}
            return response.status, payload, dict(response.headers.items())
    except HTTPError as error:
        raw = error.read().decode("utf-8", errors="replace")
        try:
            detail = json.loads(raw)
        except json.JSONDecodeError:
            detail = raw
        raise RuntimeError(f"Fabric API returned HTTP {error.code}: {detail}") from error
    except URLError as error:
        raise RuntimeError(f"Could not reach the Fabric API: {error.reason}") from error


def poll_operation(url: str, token: str, initial_headers: dict[str, str]) -> dict[str, Any]:
    operation_url = initial_headers.get("Location") or initial_headers.get("location")
    if not operation_url:
        operation_id = initial_headers.get("Operation-Id") or initial_headers.get("operation-id")
        if operation_id:
            operation_url = f"{FABRIC_API}/operations/{operation_id}"
    if not operation_url:
        raise RuntimeError("Fabric returned 202 without a Location or Operation-Id header.")

    for _ in range(120):
        status, payload, headers = request_json("GET", operation_url, token)
        state = str(payload.get("status", "")).lower()
        if status == 200 and state in {"succeeded", "completed"}:
            result_url = headers.get("Location") or headers.get("location")
            if result_url and result_url != operation_url:
                return request_json("GET", result_url, token)[1]
            return payload
        if state in {"failed", "cancelled"}:
            raise RuntimeError(f"Fabric operation {state}: {payload}")
        retry_after = int(headers.get("Retry-After", headers.get("retry-after", "2")))
        time.sleep(max(1, min(retry_after, 10)))

    raise RuntimeError(f"Fabric operation did not complete: {operation_url}")


def find_existing_model(workspace_id: str, display_name: str, token: str) -> dict[str, Any] | None:
    url = f"{FABRIC_API}/workspaces/{quote(workspace_id)}/semanticModels"
    _, payload, _ = request_json("GET", url, token)
    return next(
        (item for item in payload.get("value", []) if item.get("displayName") == display_name),
        None,
    )


def verify_workspace(workspace_id: str, token: str) -> None:
    url = f"{FABRIC_API}/workspaces/{quote(workspace_id)}"
    _, workspace, _ = request_json("GET", url, token)
    if not workspace.get("capacityId"):
        raise RuntimeError("The target workspace is not assigned to a Fabric capacity.")


def deploy(args: argparse.Namespace, parts: list[dict[str, str]]) -> str:
    if not args.workspace_id:
        raise ValueError("--workspace-id is required unless --dry-run is used.")

    token = get_access_token()
    verify_workspace(args.workspace_id, token)
    existing = find_existing_model(args.workspace_id, args.display_name, token)
    definition = {"format": "TMDL", "parts": parts}

    if existing:
        if not args.update_existing:
            raise RuntimeError(
                f"A semantic model named '{args.display_name}' already exists with ID "
                f"{existing['id']}. Re-run with --update-existing to replace its definition."
            )
        model_id = existing["id"]
        url = (
            f"{FABRIC_API}/workspaces/{quote(args.workspace_id)}/semanticModels/"
            f"{quote(model_id)}/updateDefinition"
        )
        status, payload, headers = request_json("POST", url, token, {"definition": definition})
    else:
        url = f"{FABRIC_API}/workspaces/{quote(args.workspace_id)}/semanticModels"
        status, payload, headers = request_json(
            "POST",
            url,
            token,
            {"displayName": args.display_name, "definition": definition},
        )
        model_id = payload.get("id", "")

    if status == 202:
        payload = poll_operation(url, token, headers)
        model_id = payload.get("id") or payload.get("itemId") or model_id

    deployed = find_existing_model(args.workspace_id, args.display_name, token)
    if not deployed:
        raise RuntimeError("Deployment completed, but the semantic model was not found in the workspace.")
    return str(deployed["id"])


def main() -> int:
    args = parse_args()
    try:
        model_dir = args.model_dir.resolve()
        parts = build_parts(model_dir)
        print(f"Validated {len(parts)} definition parts from {model_dir}:")
        for part in parts:
            print(f"  - {part['path']}")

        if args.dry_run:
            print("Dry run complete; no Fabric API calls were made.")
            return 0

        model_id = deploy(args, parts)
        print(f"Deployed semantic model '{args.display_name}'.")
        print(f"Semantic model ID: {model_id}")
        return 0
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
