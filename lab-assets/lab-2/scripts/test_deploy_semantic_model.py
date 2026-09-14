import subprocess
import unittest
from io import BytesIO
from pathlib import Path
from unittest import mock
from urllib.error import HTTPError

from scripts import deploy_semantic_model


class ModelDefinitionTests(unittest.TestCase):
    def test_every_table_partition_is_marked_as_a_table_result(self) -> None:
        tables_dir = deploy_semantic_model.DEFAULT_MODEL_DIR / "definition" / "tables"

        for table_path in tables_dir.glob("*.tmdl"):
            with self.subTest(table=table_path.name):
                definition = table_path.read_text()
                self.assertIn("annotation PBI_NavigationStepName = Navigation", definition)
                self.assertIn("annotation PBI_ResultType = Table", definition)


class RayfinCliTests(unittest.TestCase):
    @mock.patch.object(deploy_semantic_model.subprocess, "run")
    @mock.patch.object(deploy_semantic_model, "get_rayfin_auth_module")
    @mock.patch.object(deploy_semantic_model.shutil, "which", return_value="/usr/bin/node")
    def test_get_access_token_uses_rayfin_auth_and_trims_token(
        self,
        _which: mock.Mock,
        get_auth_module: mock.Mock,
        run: mock.Mock,
    ) -> None:
        get_auth_module.return_value = Path("/project/node_modules/@microsoft/rayfin-cli/dist/auth/index.js")
        run.return_value = subprocess.CompletedProcess([], 0, stdout=" token-value\n", stderr="")

        token = deploy_semantic_model.get_access_token()

        self.assertEqual(token, "token-value")
        command = run.call_args.args[0]
        self.assertEqual(command[0], "/usr/bin/node")
        self.assertEqual(command[1:3], ["--input-type=module", "--eval"])
        self.assertIn("silentOnly: true", command[3])
        self.assertEqual(
            command[4],
            "file:///project/node_modules/%40microsoft/rayfin-cli/dist/auth/index.js",
        )
        self.assertFalse(run.call_args.kwargs.get("shell", False))

    @mock.patch.object(deploy_semantic_model.subprocess, "run")
    @mock.patch.object(deploy_semantic_model, "get_rayfin_auth_module", return_value=Path("auth.js"))
    @mock.patch.object(deploy_semantic_model.shutil, "which", return_value="node")
    def test_get_access_token_reports_authentication_failure(
        self,
        _which: mock.Mock,
        _get_auth_module: mock.Mock,
        run: mock.Mock,
    ) -> None:
        run.side_effect = subprocess.CalledProcessError(
            1,
            ["node"],
            stderr="No cached account",
        )

        with self.assertRaisesRegex(RuntimeError, "npx rayfin login"):
            deploy_semantic_model.get_access_token()

    @mock.patch.object(deploy_semantic_model.subprocess, "run", side_effect=FileNotFoundError)
    @mock.patch.object(deploy_semantic_model, "get_rayfin_auth_module", return_value=Path("auth.js"))
    @mock.patch.object(deploy_semantic_model.shutil, "which", return_value="node")
    def test_get_access_token_reports_launch_failure(
        self,
        _which: mock.Mock,
        _get_auth_module: mock.Mock,
        _run: mock.Mock,
    ) -> None:
        with self.assertRaisesRegex(RuntimeError, "could not be launched"):
            deploy_semantic_model.get_access_token()

    @mock.patch.object(deploy_semantic_model.subprocess, "run")
    @mock.patch.object(deploy_semantic_model, "get_rayfin_auth_module", return_value=Path("auth.js"))
    @mock.patch.object(deploy_semantic_model.shutil, "which", return_value="node")
    def test_get_access_token_rejects_empty_token(
        self,
        _which: mock.Mock,
        _get_auth_module: mock.Mock,
        run: mock.Mock,
    ) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="  \n", stderr="")

        with self.assertRaisesRegex(RuntimeError, "empty Fabric access token"):
            deploy_semantic_model.get_access_token()


class FabricApiTests(unittest.TestCase):
    @mock.patch.object(deploy_semantic_model, "urlopen")
    def test_request_json_explains_empty_unauthorized_response(self, urlopen: mock.Mock) -> None:
        error = HTTPError(
            "https://api.fabric.microsoft.com/v1/test",
            401,
            "Unauthorized",
            {},
            BytesIO(b""),
        )
        self.addCleanup(error.close)
        urlopen.side_effect = error

        with self.assertRaisesRegex(
            RuntimeError,
            r"/v1/test returned HTTP 401: Unauthorized.*rayfin login",
        ):
            deploy_semantic_model.request_json(
                "GET",
                "https://api.fabric.microsoft.com/v1/test",
                "token-value",
            )

    @mock.patch.object(deploy_semantic_model, "request_json")
    def test_resolve_workspace_id_accepts_and_normalizes_guid(
        self,
        request_json: mock.Mock,
    ) -> None:
        workspace_id = deploy_semantic_model.resolve_workspace_id(
            "82599DDD-89BC-45ED-8AAD-006E2477226D",
            "token-value",
        )

        self.assertEqual(workspace_id, "82599ddd-89bc-45ed-8aad-006e2477226d")
        request_json.assert_not_called()

    @mock.patch.object(deploy_semantic_model, "request_json")
    def test_resolve_workspace_id_finds_exact_workspace_name(
        self,
        request_json: mock.Mock,
    ) -> None:
        request_json.return_value = (
            200,
            {
                "value": [
                    {"displayName": "rayfin", "id": "7fb8bec9-bb2c-437a-bbfb-efa04b6f4acb"},
                    {
                        "displayName": "ahmedbhamworkspace",
                        "id": "82599ddd-89bc-45ed-8aad-006e2477226d",
                    },
                ]
            },
            {},
        )

        workspace_id = deploy_semantic_model.resolve_workspace_id("rayfin", "token-value")

        self.assertEqual(workspace_id, "7fb8bec9-bb2c-437a-bbfb-efa04b6f4acb")

    @mock.patch.object(deploy_semantic_model, "request_json")
    def test_resolve_workspace_id_reports_missing_name(self, request_json: mock.Mock) -> None:
        request_json.return_value = (200, {"value": []}, {})

        with self.assertRaisesRegex(ValueError, "No accessible Fabric workspace"):
            deploy_semantic_model.resolve_workspace_id("missing", "token-value")

    @mock.patch.object(deploy_semantic_model, "request_json")
    def test_resolve_workspace_id_reports_duplicate_name(self, request_json: mock.Mock) -> None:
        request_json.return_value = (
            200,
            {
                "value": [
                    {"displayName": "duplicate", "id": "first-id"},
                    {"displayName": "duplicate", "id": "second-id"},
                ]
            },
            {},
        )

        with self.assertRaisesRegex(ValueError, "Multiple accessible Fabric workspaces"):
            deploy_semantic_model.resolve_workspace_id("duplicate", "token-value")

    @mock.patch.object(deploy_semantic_model, "urlopen")
    def test_request_json_normalizes_null_response(self, urlopen: mock.Mock) -> None:
        response = mock.MagicMock()
        response.status = 202
        response.read.return_value = b"null"
        response.headers.items.return_value = [("Operation-Id", "operation-id")]
        urlopen.return_value.__enter__.return_value = response

        status, payload, headers = deploy_semantic_model.request_json(
            "POST",
            "https://api.fabric.microsoft.com/v1/workspaces/id/semanticModels",
            "token-value",
            {"definition": {}},
        )

        self.assertEqual(status, 202)
        self.assertEqual(payload, {})
        self.assertEqual(headers["Operation-Id"], "operation-id")


if __name__ == "__main__":
    unittest.main()