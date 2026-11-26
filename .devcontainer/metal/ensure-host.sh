#!/usr/bin/env bash
# Runs on the Mac, before the dev container is created. Docker on macOS is a
# Linux VM, and Metal is not in that VM. This starts the process that owns
# the GPU. The container reaches it at host.docker.internal:47700.
# Safe to run again: an existing server on that port is left running.

set -euo pipefail

pin="$(cd "$(dirname "$0")/.." && pwd)/torch-pin.sh"
# shellcheck source=../torch-pin.sh
. "$pin"

if [ "$(uname -s)" != "Darwin" ] || [ "$(uname -m)" != "arm64" ]; then
  echo "The Apple MPS dev container is for a Mac with Apple silicon." >&2
  echo "On Windows with an NVIDIA GPU, reopen with Drone playground (CUDA)." >&2
  exit 1
fi

if ! command -v git >/dev/null 2>&1 || ! command -v clang++ >/dev/null 2>&1; then
  echo "git and clang++ are required. Install the Xcode command line tools: xcode-select --install" >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1 || ! command -v python3 >/dev/null 2>&1; then
  echo "curl and python3 are required." >&2
  exit 1
fi

uv_dir="${HOME}/.cache/drone-playground/bin"
if ! command -v uv >/dev/null 2>&1; then
  if [ ! -x "${uv_dir}/uv" ]; then
    echo "Installing uv into ${uv_dir}"
    mkdir -p "${uv_dir}"
    curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="${uv_dir}" UV_NO_MODIFY_PATH=1 sh
  fi
  export PATH="${uv_dir}:${PATH}"
fi

dest="${HOME}/.cache/drone-playground/varco"
if [ ! -d "${dest}/.git" ]; then
  mkdir -p "$(dirname "${dest}")"
  git clone "${VARCO_URL}" "${dest}"
fi

if [ "$(git -C "${dest}" rev-parse HEAD)" != "${VARCO_COMMIT}" ]; then
  git -C "${dest}" fetch --depth 1 origin "${VARCO_COMMIT}"
  git -C "${dest}" checkout --force --detach FETCH_HEAD
fi

"${dest}/pytorch/build-mac.sh"

# Own session: initializeCommand's process group ends when this script does.
python3 "$(cd "$(dirname "$0")" && pwd)/start-server.py" \
  "${dest}/pytorch" "${TORCH_VERSION}" "${VARCO_PORT}"
