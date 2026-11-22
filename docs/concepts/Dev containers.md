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

[[Gazebo]] and [[ROS 2 Jazzy]] expect Ubuntu. This project is edited on Windows. Installing that stack on the host, and keeping it in agreement with what runs in deployment, is most of the pain and none of the control theory. A container is a known Ubuntu.

## In this playground

`.devcontainer/devcontainer.json` opens the whole repo in one container, built from the `dev` target of `docker/Dockerfile`. Gazebo, the bridge, the controller, and the tools all run there, each in its own terminal, so a change to the law is one restart away. The image includes JupyterLab, Ruff, and mypy from `control/requirements/dev.txt`. The post-create step installs the controller package in editable mode, registers the `/opt/venv` interpreter as a Jupyter kernel, and, once the repo is a git repository, the pre-commit hooks. From `control/`, `make notebook` starts JupyterLab on port 8888.

`compose.yaml` is deployment only. It builds the `runtime` target of the same Dockerfile, copies the sources in, and starts one container per component. Nothing is mounted from the host. [[Foxglove]] stays on Windows and is optional.

## See also

- [[Fast DDS]]
- [[ROS 2 Jazzy]]
