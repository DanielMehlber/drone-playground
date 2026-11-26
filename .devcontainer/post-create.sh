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
bash .devcontainer/install-torch.sh
