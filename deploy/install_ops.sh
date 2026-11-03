#!/usr/bin/env bash
# Install the ops sync (status publisher + fix applier) as a systemd timer, every 5 minutes. Run on the instance from any repo checkout:
#   bash deploy/install_ops.sh
# Needs: git push rights to the repo (the same credentials you already push batches with), passwordless sudo for `systemctl restart`.
# Remove: sudo systemctl disable --now final-pipeline-ops.timer
set -euo pipefail
REPO="$(pwd)"; ME="$(whoami)"
sudo tee /etc/systemd/system/final-pipeline-ops.service >/dev/null <<EOF
[Unit]
Description=Final pipeline ops sync (status out, fixes in)
[Service]
Type=oneshot
User=${ME}
WorkingDirectory=${REPO}
ExecStart=/usr/bin/python3 ${REPO}/deploy/ops_sync.py
EOF
sudo tee /etc/systemd/system/final-pipeline-ops.timer >/dev/null <<EOF
[Unit]
Description=Final pipeline ops sync every 5 minutes
[Timer]
OnBootSec=2min
OnUnitActiveSec=5min
[Install]
WantedBy=timers.target
EOF
sudo systemctl daemon-reload
sudo systemctl enable --now final-pipeline-ops.timer
sudo systemctl start final-pipeline-ops.service || true
sleep 3; sudo systemctl --no-pager status final-pipeline-ops.service | head -8
