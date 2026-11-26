#!/usr/bin/env bash
# Every start. The GPU server lives on the Mac, and a container restart does
# not start it. Warn, and still let the editor open: Gazebo does not need it.

set -euo pipefail

if ! BRIDGE_TIMEOUT=2 python -c 'import torch
ok = torch.backends.mps.is_available()
if ok:
    print("MPS bridge is up.", torch.__version__)
raise SystemExit(0 if ok else 1)'; then
  echo "MPS bridge is not answering. On the Mac, run: bash .devcontainer/metal/ensure-host.sh" >&2
fi
