# Helvetia data app

Streamlit app that queries `samples.nyctaxi.trips` through a Databricks SQL warehouse.

## Run locally

Use the same Databricks CLI profile you already use for the workspace. `Config()` picks up that profile locally and the app service principal once the app is deployed — do not hardcode tokens.

```bash
# from this directory
databricks apps run-local --prepare-environment --debug \
  --env DATABRICKS_WAREHOUSE_ID=<your-warehouse-id>
```

`--prepare-environment` creates a local venv with `uv` and installs `requirements.txt`. The proxy listens on http://localhost:8001.

If you already have a warehouse named `helvetia-wh` in the workspace:

```bash
databricks warehouses list --output json | jq -r '.[] | select(.name=="helvetia-wh") | .id'
```
