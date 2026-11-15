#!/usr/bin/env bash
# Install the chain runner (TOC -> glossary -> final, every 3 minutes). Run once on the VM from the ops clone (~/ops).
set -euo pipefail
REPO="$(pwd)"; ME="$(whoami)"
sudo tee /etc/systemd/system/devspace-chain.service >/dev/null <<UNIT
[Unit]
Description=Devspace chain runner
[Service]
Type=oneshot
User=${ME}
WorkingDirectory=${REPO}
ExecStart=/usr/bin/python3 ${REPO}/deploy/chain.py
UNIT
sudo tee /etc/systemd/system/devspace-chain.timer >/dev/null <<UNIT
[Unit]
Description=Devspace chain runner every 3 minutes
[Timer]
OnBootSec=3min
OnUnitActiveSec=3min
[Install]
WantedBy=timers.target
UNIT
sudo systemctl daemon-reload
sudo systemctl enable --now devspace-chain.timer
