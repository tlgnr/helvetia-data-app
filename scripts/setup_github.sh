#!/usr/bin/env bash
# Create GitHub Environments and set DATABRICKS_HOST / DATABRICKS_CLIENT_ID
# from Terraform output. Values are variables, not secrets.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
TF_DIR="${TF_DIR:-$ROOT/infra}"
REPO="${GITHUB_REPOSITORY:-}"

if [[ -z "$REPO" ]]; then
  echo "Set GITHUB_REPOSITORY=owner/helvetia-data-app" >&2
  exit 1
fi

if ! command -v jq >/dev/null || ! command -v gh >/dev/null; then
  echo "Need gh and jq on PATH" >&2
  exit 1
fi

JSON="$(terraform -chdir="$TF_DIR" output -json github_environments)"

for env in dev test prod; do
  gh api --method PUT "repos/${REPO}/environments/${env}" >/dev/null
  host="$(echo "$JSON" | jq -r --arg e "$env" '.[$e].DATABRICKS_HOST')"
  client_id="$(echo "$JSON" | jq -r --arg e "$env" '.[$e].DATABRICKS_CLIENT_ID')"
  gh variable set DATABRICKS_HOST --env "$env" --repo "$REPO" --body "$host"
  gh variable set DATABRICKS_CLIENT_ID --env "$env" --repo "$REPO" --body "$client_id"
  echo "Configured environment $env -> $host ($client_id)"
done

echo
echo "In GitHub: Settings > Environments > prod > Required reviewers"
echo "Federation subject is repo:${REPO}:environment:<env>"
