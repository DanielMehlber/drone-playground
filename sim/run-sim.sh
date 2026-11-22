#!/usr/bin/env bash
# Gazebo server. Pass --gui to open the Gazebo window on the Windows desktop.
set -euo pipefail
set +u
source /opt/ros/jazzy/setup.bash
set -u

world="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/worlds/quadcopter.sdf"

open_browser_view() {
  export DISPLAY=:99
  export LIBGL_ALWAYS_SOFTWARE=1
  export QT_X11_NO_MITSHM=1
  if [[ ! -S /tmp/.X11-unix/X99 ]]; then
    nohup Xvfb :99 -screen 0 1280x720x24 >/tmp/xvfb.log 2>&1 &
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      [[ -S /tmp/.X11-unix/X99 ]] && break
      sleep 0.2
    done
  fi
  if ! pgrep -x x11vnc >/dev/null 2>&1; then
    nohup x11vnc -display :99 -nopw -forever -shared -rfbport 5900 >/tmp/x11vnc.log 2>&1 &
  fi
  if ! pgrep -f "websockify --web /usr/share/novnc" >/dev/null 2>&1; then
    nohup websockify --web /usr/share/novnc 6080 localhost:5900 >/tmp/novnc.log 2>&1 &
  fi
  echo "Gazebo window: http://localhost:6080/vnc.html?autoconnect=1&resize=scale"
  # OGRE 2 crashes on this software display. OGRE 1 draws the scene.
  exec gz sim -r --render-engine-gui ogre "${world}"
}

if [[ "${1:-}" == "--view" ]]; then
  open_browser_view
fi
if [[ "${1:-}" == "--gui" ]]; then
  if [[ ! -S /wslg-x11/X0 ]]; then
    echo "The Windows display socket is not mounted at /wslg-x11/X0." >&2
    exit 1
  fi
  mkdir -p /tmp/.X11-unix
  ln -sfn /wslg-x11/X0 /tmp/.X11-unix/X0
  export DISPLAY=:0
  export QT_QPA_PLATFORM=xcb
  export QT_X11_NO_MITSHM=1
  exec gz sim -r "${world}"
fi

# Server only. No window.
exec gz sim -s -r "${world}"
