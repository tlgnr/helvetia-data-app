# --- diagnostics bootstrap: install crash/exception logging before app code ---
import os as _diag_os
import sys as _diag_sys

_diag_dir = _diag_os.path.dirname(_diag_os.path.abspath(__file__))
if _diag_dir not in _diag_sys.path:
    _diag_sys.path.insert(0, _diag_dir)
import app_diagnostics  # noqa: E402

app_diagnostics.install_diagnostics()
# --- end diagnostics bootstrap ---

import os

import pandas as pd
import streamlit as st
from databricks import sql
from databricks.sdk.core import Config

assert os.getenv("DATABRICKS_WAREHOUSE_ID"), (
    "DATABRICKS_WAREHOUSE_ID must be set. For run-local, pass "
    "--env DATABRICKS_WAREHOUSE_ID=<id>. The bundle binds resource sql-warehouse."
)

_api_key = os.getenv("EXTERNAL_API_KEY", "")
assert _api_key, (
    "EXTERNAL_API_KEY is missing. Locally pass --env EXTERNAL_API_KEY=.... "
    "Deployed, the bundle maps secret scope helvetia-app / key external-api-key "
    "onto this env var. Never put the value in app.yaml or databricks.yml."
)


def mask_secret(value: str, visible: int = 4) -> str:
    if len(value) <= visible:
        return "*" * len(value)
    return "*" * (len(value) - visible) + value[-visible:]


def sql_query(query: str) -> pd.DataFrame:
    cfg = Config()
    with sql.connect(
        server_hostname=cfg.host,
        http_path=f"/sql/1.0/warehouses/{os.getenv('DATABRICKS_WAREHOUSE_ID')}",
        credentials_provider=lambda: cfg.authenticate,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall_arrow().to_pandas()


st.set_page_config(layout="wide", page_title="Helvetia taxi fares")


@st.cache_data(ttl=30)
def get_data():
    return sql_query("select * from samples.nyctaxi.trips limit 5000")


data = get_data()

st.header("Taxi fare distribution")
st.caption(f"External API key (masked): `{mask_secret(_api_key)}`")
col1, col2 = st.columns([3, 1])
with col1:
    st.scatter_chart(data=data, height=400, width=700, y="fare_amount", x="trip_distance")
with col2:
    st.subheader("Predict fare")
    pickup = st.text_input("From (zipcode)", value="10003")
    dropoff = st.text_input("To (zipcode)", value="11238")
    subset = data[(data["pickup_zip"] == int(pickup)) & (data["dropoff_zip"] == int(dropoff))]
    fare = subset["fare_amount"].mean() if len(subset) > 0 else 99
    st.write(f"# **${fare:.2f}**")

st.dataframe(data=data, height=600, use_container_width=True)
