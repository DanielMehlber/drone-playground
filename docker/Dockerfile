# syntax=docker/dockerfile:1

# base: ROS 2 Jazzy, Gazebo Harmonic, and a venv that also sees the apt ROS packages.
FROM ros:jazzy-ros-base AS base

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:/opt/ros/jazzy/bin:${PATH}

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        libegl1 \
        libgl1 \
        libgl1-mesa-dri \
        novnc \
        python3-venv \
        ros-jazzy-actuator-msgs \
        ros-jazzy-foxglove-bridge \
        ros-jazzy-ros-gz \
        ros-jazzy-sensor-msgs \
        websockify \
        x11vnc \
        xvfb \
    && rm -rf /var/lib/apt/lists/*

# rclpy needs the apt Python packages, so the venv inherits system site-packages.
# The .pth file makes the ROS packages importable even where setup.bash was not
# sourced, for example in editor tooling.
RUN python3 -m venv --system-site-packages "${VIRTUAL_ENV}" \
    && echo /opt/ros/jazzy/lib/python3.12/site-packages \
        > "${VIRTUAL_ENV}/lib/python3.12/site-packages/ros-jazzy.pth"

WORKDIR /workspaces/drone-playground

COPY control/requirements/base.txt /tmp/requirements/base.txt
RUN pip install --requirement /tmp/requirements/base.txt

RUN printf '%s\n' 'source /opt/ros/jazzy/setup.bash' >> /etc/bash.bashrc

COPY docker/ros-entrypoint.sh /usr/local/bin/ros-entrypoint.sh
RUN chmod +x /usr/local/bin/ros-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/ros-entrypoint.sh"]
CMD ["sleep", "infinity"]


# dev: the dev container. Sources are bind-mounted, not copied.
FROM base AS dev

# g++ and Python headers compile the MPS bridge into the venv on a Mac.
# That bridge is a Linux extension; the CUDA image never loads it.
RUN apt-get update && apt-get install -y --no-install-recommends \
        g++ \
        git \
        make \
        python3-dev \
        shellcheck \
    && rm -rf /var/lib/apt/lists/*

COPY control/requirements/dev.txt /tmp/requirements/dev.txt
# TORCH_INDEX empty: pip installs torch from PyPI. On linux/amd64 that wheel
# is the CUDA build the Windows container already used. The Apple MPS dev
# container sets the CPU index, because the CUDA packages are not the GPU
# on a Mac and do not install on linux/arm64. The version matches
# .devcontainer/torch-pin.sh. post-create still switches a visible NVIDIA
# GPU to the cu128 wheel.
ARG TORCH_VERSION=2.15.0
ARG TORCH_INDEX=
RUN pip install --requirement /tmp/requirements/dev.txt \
    && if [ -n "${TORCH_INDEX}" ]; then \
         pip install --upgrade "torch==${TORCH_VERSION}" \
           --index-url "${TORCH_INDEX}" \
           --extra-index-url https://pypi.org/simple; \
       else \
         pip install --upgrade "torch==${TORCH_VERSION}"; \
       fi


# runtime: what compose.yaml deploys. One image, one command per service.
FROM base AS runtime

COPY control/ control/
RUN pip install --no-deps ./control

COPY sim/ sim/
RUN chmod +x sim/*.sh control/*.sh
