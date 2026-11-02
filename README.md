# Helvetia data app

Streamlit Databricks App with a Declarative Automation Bundle and GitHub Actions CI/CD.

Authentication in GitHub is **Databricks-native OIDC** (`DATABRICKS_AUTH_TYPE=github-oidc`). There is no Databricks PAT and no Azure client secret in this repository.

## Branch and promotion model

| Event | Workflow | Workspace |
| --- | --- | --- |
| PR from a feature branch into `main` | `ci.yml` + `integration.yml` | **dev** (integration) |
| Merge into `main` | `cd-test.yml` | **test** |
| GitHub Release published | `cd-prod.yml` | **prod** (environment approval) |

## Local

```bash
cd src/app
databricks apps run-local --prepare-environment --debug \
  --env DATABRICKS_WAREHOUSE_ID=<id> \
  --env EXTERNAL_API_KEY=local-only-dummy
```

Personal bundle deploy (development mode, name prefix):

```bash
databricks bundle deploy --target personal
databricks bundle run data_app --target personal
```

## GitHub Environments

After Terraform apply:

```bash
export GITHUB_REPOSITORY=<owner>/helvetia-data-app
./scripts/setup_github.sh
```

Set a required reviewer on the `prod` environment. Host and client ID are **variables**, not secrets.

## Secret

```bash
databricks secrets put-secret helvetia-app external-api-key --host <workspace-url>
```

The bundle only references scope `helvetia-app` and key `external-api-key`.
