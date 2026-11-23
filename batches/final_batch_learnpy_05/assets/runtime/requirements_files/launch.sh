#!/bin/sh
set -eu
HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$HERE/root/workspace/order_report"
export PWD=/workspace/order_report
unset PYTHONHOME PYTHONPATH
export PIP_CONFIG_FILE=/workspace/order_report/pip.conf
if [ "$#" -eq 0 ]; then set -- /bin/bash --noprofile --norc; fi
exec "$HERE/../path_runtime" "$HERE/root" "$@"
