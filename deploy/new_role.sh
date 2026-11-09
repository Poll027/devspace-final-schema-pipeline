#!/usr/bin/env bash
# Create an isolated working folder for one role on the pipeline VM: its own clone of each pipeline repo, so a code fix pulled for one role can
# never trip another role's integrity guard, and each role has its own .env / cost logs / run.log.
#
#   bash deploy/new_role.sh react_frontend_developer
#
# Layout (ROLES_DIR defaults to ~/roles):
#   ~/roles/<role>/toc/       clone of universal-toc-pipeline      (TOC runs here)
#   ~/roles/<role>/glossary/  clone of devspace-glossary-pipeline  (reads ../toc workspace)
#   ~/roles/<role>/final/     clone of devspace-final-schema-pipeline (reads ../glossary bundle and ../toc workspace)
# Each clone gets a copy of the shared secrets file ~/.pipeline.env (Azure endpoint + key; create it once, chmod 600).
# Stages run in order toc -> glossary -> final; run each as its own systemd service (deploy/install_service.sh inside that clone).
# Untested until the VM exists: read before running.
set -euo pipefail
ROLE="${1:?usage: new_role.sh <path_id>}"
ROLES_DIR="${ROLES_DIR:-$HOME/roles}"
ORG="${GIT_ORG:-Poll027}"
[ -f "$HOME/.pipeline.env" ] || { echo "create ~/.pipeline.env first (copy .env.example, fill in the Azure endpoint and key, chmod 600)"; exit 1; }

mkdir -p "$ROLES_DIR/$ROLE"
clone() {  # <folder> <repo> [branch]
  if [ -d "$ROLES_DIR/$ROLE/$1/.git" ]; then echo "$1: already cloned"; return; fi
  git clone -q ${3:+-b "$3"} "https://github.com/$ORG/$2.git" "$ROLES_DIR/$ROLE/$1"
  cp "$HOME/.pipeline.env" "$ROLES_DIR/$ROLE/$1/.env"; chmod 600 "$ROLES_DIR/$ROLE/$1/.env"
  echo "$1: cloned $2${3:+ (branch $3)}"
}
clone toc universal-toc-pipeline "${TOC_BRANCH:-glm-pilot}"  # the Azure TOC driver lives on this branch
clone glossary devspace-glossary-pipeline
clone final devspace-final-schema-pipeline
echo "ready: $ROLES_DIR/$ROLE  (clone auth: the VM needs a GitHub token or deploy key with read access to these repos)"
