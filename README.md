# Helvetia data app

Declarative Automation Bundle that deploys the Streamlit app plus its warehouse and secret bindings.

The secret **value** is not in this repository. The bundle names a scope and key; Databricks Apps injects it as `EXTERNAL_API_KEY`.

## One-time: store the secret

```bash
databricks secrets put-secret helvetia-app external-api-key
```

Use a dummy value for the demo. Terraform created the `helvetia-app` scope; this command only writes the key.

## Deploy with the bundle

```bash
databricks bundle validate --strict --target dev
databricks bundle deploy --target dev
databricks bundle run data_app --target dev
databricks apps logs helvetia-data-app-dev
```

`warehouse_id` is resolved with `lookup` against a warehouse named `helvetia-wh`. `app.yaml` still uses `valueFrom`, never a hardcoded warehouse ID or secret.

For `test` and `prod`:

```bash
databricks bundle deploy --target test --var deploy_sp_client_id=<sp-application-id>
databricks bundle run data_app --target test --var deploy_sp_client_id=<sp-application-id>
```

## Run locally

```bash
cd src/app
databricks apps run-local --prepare-environment --debug \
  --env DATABRICKS_WAREHOUSE_ID=<your-warehouse-id> \
  --env EXTERNAL_API_KEY=local-only-dummy
```
