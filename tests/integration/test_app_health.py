import os

import pytest
from databricks import sql
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config


APP_NAME = os.getenv("APP_NAME", "helvetia-data-app-dev")
WAREHOUSE_ID = os.getenv("DATABRICKS_WAREHOUSE_ID", "")


@pytest.fixture(scope="module")
def w() -> WorkspaceClient:
    return WorkspaceClient()


def test_app_is_running(w: WorkspaceClient):
    app = w.apps.get(APP_NAME)
    state = getattr(getattr(app, "app_status", None), "state", None) or getattr(
        app, "compute_status", None
    )
    assert str(state).upper().endswith("RUNNING") or str(state).upper() == "RUNNING", (
        f"app {APP_NAME} is not RUNNING: {state}"
    )


def test_warehouse_query_succeeds():
    if not WAREHOUSE_ID:
        pytest.skip("DATABRICKS_WAREHOUSE_ID not set")
    cfg = Config()
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{WAREHOUSE_ID}",
        credentials_provider=lambda: cfg.authenticate,
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute("select 1 as ok")
            row = cursor.fetchone()
            assert row[0] == 1
