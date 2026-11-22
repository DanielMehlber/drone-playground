---
type: concept
module: simulation
tags:
  - concept
  - simulation
status: article
aliases:
  - SITL
---

# Software in the loop

Software-in-the-loop means the flight program you intend to ship is running as an ordinary process, against a simulated aircraft. The drivers that would talk to chips are replaced by the simulator. The estimator and the controller are the real ones. Aerospace programs have done this for decades, long before small drones. The acronym is SITL.

## The problem

Developing on the [[Flight controller]] is slow, and a mistake commands real motors. A pure numerical toy of the aircraft is fast, and then you rewrite everything to fit the autopilot. SITL keeps the autopilot binary and swaps only the plant.

## In this playground

This repo simulates the plant and runs your controller beside it. That is software-in-the-loop for the law you are writing, not for a stock autopilot. [[PX4 Autopilot]] SITL would be the other kind: the firmware binary in the loop, and your code only sending setpoints. Hardware-in-the-loop, a real board on the desk, is later. The ROS topics are the seam either way.

## See also

- [[Autopilot]]
- [[Gazebo]]
