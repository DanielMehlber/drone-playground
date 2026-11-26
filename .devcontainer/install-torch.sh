#!/usr/bin/env bash
# Select the PyTorch build for this container.
# CUDA when an NVIDIA GPU was passed in. The Apple MPS dev container sets
# HOST_GPU=mps and keeps the CPU wheel, then loads the Metal bridge.
# pip-sync drops torch, because it is not in requirements/dev.txt; this puts
# it back. A container with neither GPU keeps the wheel the image already has.

set -euo pipefail

pin="$(cd "$(dirname "$0")" && pwd)/torch-pin.sh"
# shellcheck source=torch-pin.sh
. "$pin"

if [ "${HOST_GPU:-}" = "mps" ]; then
  bash "$(cd "$(dirname "$0")" && pwd)/metal/install-bridge.sh"
elif command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1; then
  echo "NVIDIA GPU is visible. Installing the CUDA build of PyTorch ${TORCH_VERSION}."
  # Index only: an extra PyPI index can resolve a different CUDA build of the same version.
  if ! pip install --upgrade "torch==${TORCH_VERSION}" --index-url "${TORCH_CUDA_INDEX}"; then
    echo "CUDA PyTorch install failed. The CPU build remains installed."
  fi
else
  echo "No NVIDIA GPU is visible in this container."
  echo "Recreate the dev container after Docker can pass a GPU. Restarting this container will not."
  if ! BRIDGE=0 python -c "import torch" >/dev/null 2>&1; then
    echo "Installing the CPU build of PyTorch ${TORCH_VERSION}."
    pip install --upgrade "torch==${TORCH_VERSION}" --index-url "${TORCH_CPU_INDEX}" --extra-index-url https://pypi.org/simple
  fi
fi

BRIDGE=0 python -c 'import torch; print("torch", torch.__version__, "cuda", torch.version.cuda)'
