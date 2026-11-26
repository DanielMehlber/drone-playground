#!/usr/bin/env python3
"""Start the Mac MPS server in its own session.

The dev container runs ensure-host.sh and then waits for that script to
exit. A server left in the script's process group is killed with it. A new
session keeps the GPU process after the script is gone.
"""

from __future__ import annotations

import os
import socket
import subprocess
import sys
import time


def listening(port: int) -> bool:
    with socket.socket() as sock:
        sock.settimeout(0.2)
        try:
            sock.connect(("127.0.0.1", port))
        except OSError:
            return False
    return True


def main() -> None:
    root, version, port_text = sys.argv[1:]
    port = int(port_text)
    if listening(port):
        print(f"PyTorch MPS bridge is already listening on 127.0.0.1:{port}.")
        return

    python = os.path.join(root, f".venv-mac-{version}", "bin", "python")
    if not os.access(python, os.X_OK):
        sys.exit(f"no {python}: the Mac side of the bridge did not build")

    runs = os.path.join(root, "runs")
    os.makedirs(runs, exist_ok=True)
    log_path = os.path.join(runs, "server.log")
    env = os.environ.copy()
    env["HF_HUB_OFFLINE"] = "1"
    env["TRANSFORMERS_VERBOSITY"] = "error"
    with open(log_path, "w") as log:
        process = subprocess.Popen(
            [python, "-m", "bridge.server", str(port)],
            cwd=root,
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=env,
        )
    with open(os.path.join(runs, "server.pid"), "w") as pid_file:
        pid_file.write(f"{process.pid}\n")

    deadline = time.time() + 30
    while time.time() < deadline:
        if listening(port):
            with open(log_path) as log:
                line = log.readline().strip()
            print(line or f"bridge server listening on 127.0.0.1:{port} (process {process.pid})")
            return
        if process.poll() is not None:
            with open(log_path) as log:
                sys.stdout.write(log.read())
            sys.exit(f"bridge server exited with status {process.returncode}")
        time.sleep(0.2)
    sys.exit("bridge server did not open its port")


if __name__ == "__main__":
    main()
