#!/usr/bin/env bash
# Optional. Foxglove on Windows connects to ws://localhost:8765.
set -euo pipefail
set +u
source /opt/ros/jazzy/setup.bash
set -u
exec ros2 run foxglove_bridge foxglove_bridge
