#!/usr/bin/env bash
set -euo pipefail

pip install --no-deps --editable ./control

# Same interpreter as the editor: SymPy, editable drone_control, ROS via system site-packages.
python -m ipykernel install --user --name=drone-playground --display-name="Python (drone-playground)"

if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git config --global --add safe.directory "$(pwd)"
  pre-commit install
else
  echo "Not a git repository yet. After 'git init', run 'pre-commit install'."
fi

jupyter --version

# --gpus all is a create-time flag. A restart of an existing container does not
# attach a GPU that was missing when the container was created.
if command -v nvidia-smi >/dev/null 2>&1 && nvidia-smi -L >/dev/null 2>&1; then
  echo "NVIDIA GPU is visible. Installing the CUDA build of PyTorch 2.15."
  if ! pip install --upgrade "torch==2.15.0" --index-url https://download.pytorch.org/whl/cu128; then
    echo "CUDA PyTorch install failed. The CPU build remains installed."
  fi
else
  echo "No NVIDIA GPU is visible in this container."
  echo "Recreate the dev container after Docker can pass a GPU. Restarting this container will not."
fi