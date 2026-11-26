# Drone playground

Gazebo is the aircraft and the room. One Python program is the inner loop: it reads the IMU, magnetometer, barometer, and GNSS, and writes four rotor speeds. ROS 2 is only the cable between them. A flight path comes later, as another publisher of setpoints. It is not in this setup.

Open this folder as an Obsidian vault. Start at [docs/Home.md](docs/Home.md).

## Layout

| Folder | What it is |
|---|---|
| `sim` | Gazebo Harmonic world and the `ros_gz_bridge` script |
| `control` | The Python controller package, `drone_control` |
| `docker` | One Dockerfile with `dev` and `runtime` targets |
| `.devcontainer` | Dev container for the whole repo: CUDA on Windows, Apple MPS on a Mac |

## Develop

1. Install Docker Desktop and the Dev Containers extension.
2. Open the repo root and choose **Reopen in Container**. Pick **Drone playground (CUDA)** on Windows with an NVIDIA GPU, or **Drone playground (Apple MPS)** on a Mac with Apple silicon. The first build is large: ROS 2 Jazzy and Gazebo Harmonic. The Mac choice also builds a PyTorch server on the host the first time. That needs the Xcode command line tools and network.
3. Start each component in its own terminal:

   ```bash
   sim/run-sim.sh            # Gazebo, headless. --view: browser at localhost:6080. --gui: WSLg window.
   sim/run-bridge.sh         # Gazebo <-> ROS topics
   drone-control             # the controller
   control/run-foxglove.sh   # optional, Foxglove on ws://localhost:8765
   ```

4. Before committing, from `control/`: `make check`.

The CUDA container mounts the WSLg X11 socket from `\\wsl$\Ubuntu` for `--gui`. Without that Ubuntu distribution, use `--view`. On a Mac, use `--view` (localhost:6080). Metal does not enter the Linux VM, so the MPS container runs a tensor on `"mps"` by sending the PyTorch operation to a server on the Mac.

## Tooling

| Tool | Role |
|---|---|
| pip-tools | `control/pyproject.toml` lists dependencies; `make lock` writes the pinned `requirements/*.txt` |
| ruff | formatter and linter |
| mypy | `--strict` type checking |
| pre-commit | runs the above, shellcheck, and file hygiene on commit |
| shellcheck | the shell scripts |

ROS packages, `rclpy` included, come from apt in the image. The venv at `/opt/venv` sees them through system site-packages.

The repo is not a git repository yet. After `git init`, run `pre-commit install` once.

## Deploy

```bash
docker compose up --build -d                    # sim, bridge, control
docker compose --profile tools up --build -d    # plus Foxglove
```

Compose builds the `runtime` image with the sources copied in. Nothing is mounted from the host, so rebuild after a change.

The containers from the earlier two-container setup still use the `drone-playground` project name. Run `docker compose down --remove-orphans` once before the first deployment.
