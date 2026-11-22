---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# Autopilot

An autopilot is the software that holds an aircraft's attitude and, often, its position, without a person moving the stick for every correction. The word is from crewed aviation in the early twentieth century. On a [[Quadrotor]] it means the program on the [[Flight controller]]: read sensors, estimate attitude, run the [[Cascade control|control cascade]], mix torques into motor speeds.

## The problem

Four motors must be updated far faster than a person can think, using sensors that are noisy and biased. Someone has to close that loop or the aircraft is a free body with fans on it.

## What you use it for

You can leave the whole cascade to the autopilot and only send waypoints. This playground does the other thing. [[PX4 Autopilot|PX4]] still runs, so you have a known-good estimate and a known-good flight to compare against, and your own nodes take over the motors through [[Offboard mode]].

Two open autopilots dominate small research drones. PX4 grew out of ETH Zurich's PIXHAWK work in the early 2010s. ArduPilot started in 2009 from the DIY Drones community. This repo uses PX4 because its [[ROS 2]] path and its Gazebo simulation are packaged together.

## See also

- [[EKF2]]
- [[Arming and failsafe]]
