#!/usr/bin/env bash
# Install the supervisor as a systemd service on the pipeline VM. Run from the repo root.
# The Azure endpoint and key live in <repo>/.env (gitignored; see .env.example), which the driver reads itself.
#   export MAX_USD=300 NOTIFY_WEBHOOK_URL=https://hooks.slack.com/...   (the webhook is optional)
#   bash deploy/install_service.sh batches/<batch_id>            (service "final-pipeline")
#   SERVICE=final-pipeline-pandas bash deploy/install_service.sh batches/<other_batch_id>   (a second batch in parallel: any new service name)
# It starts at boot and after a crash. It does NOT restart on exit codes 2/3 (needs-you / spend-cap): those mean a human must act.
# Stop a manual run first (pkill -f run_pipeline): two drivers on one batch would collide.
# Logs: journalctl -u final-pipeline -f   |   run.log in the repo root   |   bash deploy/status.sh
# Control: sudo systemctl stop|start|restart final-pipeline
set -euo pipefail
BATCH="${1:?usage: install_service.sh batches/<batch_id>}"
REPO="$(pwd)"; ME="$(whoami)"; SERVICE="${SERVICE:-final-pipeline}"
[ -f "$REPO/.env" ] || { echo "missing $REPO/.env (copy .env.example and fill in the Azure endpoint and key)"; exit 1; }

sudo tee /etc/${SERVICE}.env >/dev/null <<EOF
MAX_USD=${MAX_USD:-300}
NOTIFY_WEBHOOK_URL=${NOTIFY_WEBHOOK_URL:-}
DRIVER_ARGS=${DRIVER_ARGS:-}
EOF

sudo tee /etc/systemd/system/${SERVICE}.service >/dev/null <<EOF
[Unit]
Description=Final pipeline supervisor (${SERVICE})
After=network-online.target
Wants=network-online.target

[Service]
User=${ME}
WorkingDirectory=${REPO}
EnvironmentFile=/etc/${SERVICE}.env
ExecStartPre=/usr/bin/git -C ${REPO} checkout -- 00_FINAL_PIPELINE_CORE 01_FINAL_PACK_TEMPLATE deploy
ExecStartPre=/bin/bash ${REPO}/deploy/prepare.sh
TimeoutStartSec=900
ExecStart=${HOME}/env/bin/python ${REPO}/deploy/supervisor.py ${BATCH}
Restart=on-failure
RestartSec=60
RestartPreventExitStatus=2 3

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now ${SERVICE}
sleep 2
sudo systemctl --no-pager status ${SERVICE} | head -8
