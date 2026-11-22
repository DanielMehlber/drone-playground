#!/usr/bin/env bash
set -euo pipefail
set +u
set -a
source /opt/ros/jazzy/setup.bash
set +a
set -u
exec "$@"
