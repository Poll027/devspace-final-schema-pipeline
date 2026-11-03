#!/usr/bin/env bash
# Install the sandbox's node packages when package-lock.json or fetch_packages.mjs changed since the last time (run before every service start
# and after an ops pull). A fresh clone or a pull that adds a dependency (hyperformula, matplotlib...) otherwise crashes the startup selftest.
set -euo pipefail
cd "$(dirname "$0")/../00_FINAL_PIPELINE_CORE/sandbox"
h=$(cat package-lock.json fetch_packages.mjs | sha256sum | cut -d' ' -f1)
[ "$(cat node_modules/.prep_hash 2>/dev/null || true)" = "$h" ] && exit 0
npm ci --silent
node fetch_packages.mjs
echo "$h" > node_modules/.prep_hash
