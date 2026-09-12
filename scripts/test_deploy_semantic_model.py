import subprocess
import unittest
from unittest import mock

from scripts import deploy_semantic_model


class AzureCliTests(unittest.TestCase):
    @mock.patch.object(deploy_semantic_model.shutil, "which")
    def test_get_az_executable_returns_resolved_path(self, which: mock.Mock) -> None:
        which.return_value = r"C:\Program Files\Azure CLI\az.CMD"

        executable = deploy_semantic_model.get_az_executable()

        self.assertEqual(executable, r"C:\Program Files\Azure CLI\az.CMD")
        which.assert_called_once_with("az")

    @mock.patch.object(deploy_semantic_model.shutil, "which", return_value=None)
    def test_get_az_executable_reports_missing_cli(self, _which: mock.Mock) -> None:
        with self.assertRaisesRegex(RuntimeError, "fully restart VS Code"):
            deploy_semantic_model.get_az_executable()

    @mock.patch.object(deploy_semantic_model.subprocess, "run")
    @mock.patch.object(deploy_semantic_model, "get_az_executable")
    def test_get_access_token_uses_resolved_path_and_trims_token(
        self,
        get_executable: mock.Mock,
        run: mock.Mock,
    ) -> None:
        get_executable.return_value = r"C:\Program Files\Azure CLI\az.CMD"
        run.return_value = subprocess.CompletedProcess([], 0, stdout=" token-value\n", stderr="")

        token = deploy_semantic_model.get_access_token()

        self.assertEqual(token, "token-value")
        command = run.call_args.args[0]
        self.assertEqual(command[0], get_executable.return_value)
        self.assertEqual(command[1:4], ["account", "get-access-token", "--resource"])
        self.assertEqual(command[4], deploy_semantic_model.FABRIC_RESOURCE)
        self.assertFalse(run.call_args.kwargs.get("shell", False))

    @mock.patch.object(deploy_semantic_model.subprocess, "run")
    @mock.patch.object(deploy_semantic_model, "get_az_executable", return_value="az.CMD")
    def test_get_access_token_reports_authentication_failure(
        self,
        _get_executable: mock.Mock,
        run: mock.Mock,
    ) -> None:
        run.side_effect = subprocess.CalledProcessError(
            1,
            ["az.CMD"],
            stderr="Please run az login",
        )

        with self.assertRaisesRegex(RuntimeError, "Please run az login"):
            deploy_semantic_model.get_access_token()

    @mock.patch.object(deploy_semantic_model.subprocess, "run", side_effect=FileNotFoundError)
    @mock.patch.object(deploy_semantic_model, "get_az_executable", return_value="az.CMD")
    def test_get_access_token_reports_launch_failure(
        self,
        _get_executable: mock.Mock,
        _run: mock.Mock,
    ) -> None:
        with self.assertRaisesRegex(RuntimeError, "could not be launched"):
            deploy_semantic_model.get_access_token()

    @mock.patch.object(deploy_semantic_model.subprocess, "run")
    @mock.patch.object(deploy_semantic_model, "get_az_executable", return_value="az.CMD")
    def test_get_access_token_rejects_empty_token(
        self,
        _get_executable: mock.Mock,
        run: mock.Mock,
    ) -> None:
        run.return_value = subprocess.CompletedProcess([], 0, stdout="  \n", stderr="")

        with self.assertRaisesRegex(RuntimeError, "empty Fabric access token"):
            deploy_semantic_model.get_access_token()


class FabricApiTests(unittest.TestCase):
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