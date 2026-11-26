#!/usr/bin/env bash
# Container side of the MPS bridge. Metal does not exist in this Linux VM.
# The extension registers an "mps" device whose operations run on the Mac,
# where .devcontainer/metal/ensure-host.sh has started the server.
# The CPU wheel is required: the CUDA wheel has no such hook.

set -euo pipefail

pin="$(cd "$(dirname "$0")/.." && pwd)/torch-pin.sh"
# shellcheck source=../torch-pin.sh
. "$pin"

src=/opt/varco/pytorch/bridge
if [ ! -f "${src}/native.cpp" ]; then
  echo "Varco is not mounted at /opt/varco." >&2
  echo "Open the Apple MPS dev container. It runs .devcontainer/metal/ensure-host.sh before the container is created." >&2
  exit 1
fi

if ! command -v g++ >/dev/null 2>&1; then
  echo "g++ is not installed in this image. Rebuild the dev container." >&2
  exit 1
fi

site="$(python -c "import sysconfig; print(sysconfig.get_paths()['purelib'])")"
rm -f "${site}/bridge.pth"
rm -f "${site}"/bridge_native*.so

# BRIDGE=0: a leftover .pth must not load while torch itself is being checked.
cpu_torch() {
  BRIDGE=0 python -c 'import sys, torch; raise SystemExit(0 if torch.__version__.split("+")[0] == sys.argv[1] and not torch.version.cuda else 1)' "${TORCH_VERSION}"
}

if ! cpu_torch >/dev/null 2>&1; then
  echo "Installing the CPU build of PyTorch ${TORCH_VERSION} for the MPS bridge."
  pip install --upgrade "torch==${TORCH_VERSION}" \
    --index-url "${TORCH_CPU_INDEX}" \
    --extra-index-url https://pypi.org/simple
  if ! cpu_torch; then
    echo "The CPU wheel of PyTorch ${TORCH_VERSION} did not install." >&2
    exit 1
  fi
fi

torch_dir="$(BRIDGE=0 python -c "import os, torch; print(os.path.dirname(torch.__file__))")"
py_include="$(python -c "import sysconfig; print(sysconfig.get_paths()['include'])")"
ext_suffix="$(python -c "import sysconfig; print(sysconfig.get_config_var('EXT_SUFFIX'))")"
abi="$(BRIDGE=0 python -c "import torch; print(int(torch.compiled_with_cxx11_abi()))")"

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp "${src}/native.cpp" "${work}/native.cpp"
cp "${src}/ops/mps_ops-${TORCH_VERSION}.inc" "${work}/mps_ops.inc"

g++ -shared -fPIC -O2 -std=c++20 "-D_GLIBCXX_USE_CXX11_ABI=${abi}" \
  -I"${torch_dir}/include" -I"${torch_dir}/include/torch/csrc/api/include" -I"${py_include}" \
  "${work}/native.cpp" -o "${site}/bridge_native${ext_suffix}" \
  -L"${torch_dir}/lib" -ltorch -ltorch_cpu -lc10 -ltorch_python -Wl,-rpath,"${torch_dir}/lib"

rm -rf "${site}/bridge"
mkdir -p "${site}/bridge"
cp "${src}/"*.py "${site}/bridge/"
cp -R "${src}/ops" "${site}/bridge/ops"
echo "import bridge.auto" > "${site}/bridge.pth"

if ! python - <<'PY'
import torch

print("torch", torch.__version__, "mps", torch.backends.mps.is_available())
if not torch.backends.mps.is_available():
    raise SystemExit("MPS is not available. The server on the Mac should be listening on 127.0.0.1:47700.")
value = torch.ones(4, device="mps").sum().item()
if value != 4:
    raise SystemExit(f"MPS sum was {value}, expected 4")
print("MPS bridge ok")
PY
then
  if [ -f /opt/varco/pytorch/runs/server.log ]; then
    echo "---- bridge server log ----" >&2
    cat /opt/varco/pytorch/runs/server.log >&2
  fi
  exit 1
fi
