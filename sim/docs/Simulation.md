---
type: module
module: simulation
tags:
  - module
---

# Simulation

Gazebo integrates a [[Rigid-body quadrotor]] and publishes the sensors a small aircraft usually carries. Your controller never talks to Gazebo. [[ROS 2]] does, through `ros_gz_bridge`.

## The problem

A control law needs a plant that already has mass, drag, rotor lag, and noisy sensors. Writing that plant is a different project. This folder is the plant.

## What is in the world

`worlds/quadcopter.sdf` is one quadrotor on a ground plane. The mass, inertia, and rotor positions are the Open Robotics X3: 1.5 kg, four rotors, spin directions alternating. Visuals are boxes and disks so the first start does not download a mesh.

| Topic | What it is |
|---|---|
| `/imu` | [[IMU]], about 400 Hz, small Gaussian noise on rate and specific force |
| `/magnetometer` | [[Magnetometer]] |
| `/air_pressure` | [[Barometer]] |
| `/navsat` | [[GNSS]], origin near Zurich, world frame ENU |
| `/X3/gazebo/command/motor_speed` | four rotor speeds in rad/s |

Indices 0 and 1 turn CCW, 2 and 3 turn CW. The plugin caps each speed at 800 rad/s. Thrust of one rotor is `8.54858e-06 * omega²` newtons. Yaw torque is `0.016` times that thrust. Equal speeds near 656 rad/s hold the weight. The controller does not send that until you write the loop.

Gazebo and ROS both use z-up. Body axes are forward-left-up. There is no NED conversion in this setup. See [[Coordinate frames]] and [[REP-103]].

## Run

```bash
./run-sim.sh
./run-bridge.sh
```

`./run-sim.sh --gui` opens the Gazebo window when a display exists. Headless is the reliable mode on Docker Desktop.

`gz topic -l` lists what the simulator is actually publishing. If a sensor is missing from `ros2 topic echo`, the bridge arguments in `run-bridge.sh` are the line to change. A scene, wind, or a second vehicle is another SDF file in `worlds/`.

## See also

- [[Gazebo]]
- [[SDF]]
- [[Motor model]]
- [[Control]]
