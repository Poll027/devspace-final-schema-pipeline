#!/usr/bin/env bash
# Install the sandbox's node packages when package-lock.json or fetch_packages.mjs changed since the last time (run before every service start
# and after an ops pull). A fresh clone or a pull that adds a dependency (hyperformula, matplotlib...) otherwise crashes the startup selftest.
# Every clone's sandbox/node_modules is a symlink to ONE shared directory, and many services start (and ops pulls run) at the same time:
# unserialized, concurrent `npm ci` runs delete each other's files and leave the shared directory empty/partial (runner crashes: MODULE_NOT_FOUND,
# DuckDB-WASM unavailable). So the check-and-install is done under one exclusive lock, re-checking the hash once the lock is held.
set -euo pipefail
cd "$(dirname "$0")/../00_FINAL_PIPELINE_CORE/sandbox"
h=$(cat package-lock.json fetch_packages.mjs | sha256sum | cut -d' ' -f1)
ok() { [ "$(cat node_modules/.prep_hash 2>/dev/null || true)" = "$h" ] && [ -d node_modules/hyperformula ]; }
ok && exit 0
exec 9>"${PREPARE_LOCK:-${HOME:-/tmp}/.devspace_sandbox_prepare.lock}"
flock 9
ok && exit 0   # another service finished the install while we waited
rm -f node_modules/.prep_hash
npm ci --silent
node fetch_packages.mjs
echo "$h" > node_modules/.prep_hash
