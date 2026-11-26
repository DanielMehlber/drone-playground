---
type: concept
module: playground
tags:
  - concept
  - playground
status: article
aliases:
  - dev container
---

# Dev containers

A dev container is a Docker container that an editor opens as the machine you work on. Docker, the runtime, was released in 2013. Compose, the file that starts several containers together, came from Fig and was absorbed by Docker in 2014. Visual Studio Code's container workflow, and the open dev container spec, date from about 2019.

## The problem

[[Gazebo]] and [[ROS 2 Jazzy]] expect Ubuntu. This project is edited on Windows, with an NVIDIA GPU, and on a Mac, with Apple silicon. Installing that stack on the host, and keeping it in agreement with what runs in deployment, is most of the pain and none of the control theory. A container is a known Ubuntu. The GPU is the part that is not the same on both machines: CUDA is passed into the Linux container, and Metal is not.

## In this playground

Reopen in Container asks which file to use. `.devcontainer/cuda/devcontainer.json` is the Windows machine. It starts the container with `--gpus all` and mounts the WSLg socket, so `sim/run-sim.sh --gui` can open a window. `.devcontainer/metal/devcontainer.json` is the Mac. It does not pass `--gpus`, because Docker Desktop rejects that request when there is no NVIDIA runtime. Both build the `dev` target of `docker/Dockerfile`.

PyTorch is 2.15.0 in both, and it is not in `control/requirements/dev.txt`. The CUDA image installs the PyPI wheel, which on linux/amd64 is the CUDA build, and the post-create step switches it to the cu128 wheel once `nvidia-smi` can see a GPU. The Mac image installs the CPU wheel. Metal has no driver in the Linux VM, so before the container is created the Mac config builds a small PyTorch server on the host (varco, pinned in `.devcontainer/torch-pin.sh`) and listens on `127.0.0.1:47700`. After create, the venv loads a bridge that answers `torch.backends.mps` by sending the operation to that server. A tensor on `"mps"` runs on the Mac's GPU. The server stays up across a later reopen; run `.devcontainer/metal/ensure-host.sh` if it was stopped. MPS has no float64. The dynamics study keeps the stored float64 CUDA grid and times the same operators on MPS in float32, with the state left in the shared allocation.

Gazebo, the ROS bridge, the controller, and the tools all run in that one container, each in its own terminal, so a change to the law is one restart away. The image includes JupyterLab, Ruff, and mypy from `control/requirements/dev.txt`. The post-create step installs the controller package in editable mode, registers the `/opt/venv` interpreter as a Jupyter kernel, and, once the repo is a git repository, the pre-commit hooks. From `control/`, `make notebook` starts JupyterLab on port 8888.

`compose.yaml` is deployment only. It builds the `runtime` target of the same Dockerfile, copies the sources in, and starts one container per component. Nothing is mounted from the host. [[Foxglove]] stays on Windows and is optional.

## See also

- [[Fast DDS]]
- [[ROS 2 Jazzy]]
