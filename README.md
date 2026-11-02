# Helvetia data app

Streamlit app that queries `samples.nyctaxi.trips` through a Databricks SQL warehouse.

The app code is unchanged from local development. This step deploys it to a Databricks workspace with the CLI.

There is no `databricks apps sync` command. Upload with `databricks sync`, then deploy the app from that workspace path.

## 1. Create the app (once)

```bash
databricks apps create helvetia-data-app --json '{
  "description": "Helvetia taxi fare Streamlit app"
}'
```

Bind the SQL warehouse in the UI: **Compute > Apps > helvetia-data-app > Edit > Resources > SQL warehouse**, key `sql-warehouse` (must match `valueFrom` in `app.yaml`). Grant **Can use**.

## 2. Upload source

```bash
# replace the workspace path with your user folder
SOURCE=/Workspace/Users/<you>@<company>/helvetia-data-app
databricks sync --watch . "$SOURCE"
```

`--watch` keeps uploading as you edit. For a one-shot upload:

```bash
databricks sync . "$SOURCE"
```

## 3. Deploy and inspect

```bash
databricks apps deploy helvetia-data-app --source-code-path "$SOURCE"
databricks apps get helvetia-data-app
databricks apps logs helvetia-data-app
```

Open the URL from `databricks apps get`. Auth inside the app is still `Config()` — on the platform that is the app service principal, not your laptop profile.

## Run locally (still valid)

```bash
databricks apps run-local --prepare-environment --debug \
  --env DATABRICKS_WAREHOUSE_ID=<your-warehouse-id>
```
