---
type: concept
module: flight
tags:
  - concept
  - flight
status: article
---

# Companion computer

A companion computer is a second computer carried beside the [[Flight controller]]. It is a Linux board or a small PC. It has room for [[ROS 2]], logs, and cameras. The flight controller still runs the fastest loops. The companion runs the programs you can afford to restart.

## The problem

A microcontroller has tight memory and a deadline. Developing a new filter or a new controller there means long rebuilds, and a fault can command the motors. A second computer lets those programs be ordinary processes, logged and plotted, while [[Arming and failsafe]] stays on the autopilot.

## Background

The setup became ordinary in the early 2010s, when a small Linux board was light enough to fly and a serial link or [[MAVLink]] could join it to a [[Pixhawk]]. Since PX4 1.14 (2023) the usual join for [[ROS 2]] is [[Micro XRCE-DDS]].

## In this playground

The `control` container plays this role for the lab. It is the computer that sees the sensors and commands the rotors. On a real aircraft this is often a second board next to the [[Flight controller]], and the fast rate loop may move off it later.

## See also

- [[Offboard mode]]
- [[Bridge]]
