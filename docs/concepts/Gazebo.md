---
type: concept
module: simulation
tags:
  - concept
  - simulation
status: article
---

# Gazebo

Gazebo is a robot simulator. It moves rigid bodies, applies contacts and gravity, and renders sensors such as cameras and lidar. You describe a world and a robot in [[SDF]] files. The physics is the product. The picture on screen is there so you can see whether the physics did what you asked.

## The problem

A [[Quadrotor]] controller needs a body that falls, tilts, and hits things, plus sensors with delays and noise. Building that engine is a different job from designing the controller. Gazebo is a maintained engine so the controller can be the thing you write.

## Background

Nathan Koenig started Gazebo at the University of Southern California in 2002. It later moved to the Open Source Robotics Foundation, the same organization as [[ROS 2]]. A rewrite called Ignition began around 2017. In 2022 that line was renamed Gazebo again, and the old program became Gazebo Classic. Gazebo Harmonic, the release this repo runs, came out in September 2023 and is a long-term support line. [[ROS 2 Jazzy]] recommends it.

## In this playground

[[Simulation]] starts Gazebo Harmonic on `sim/worlds/quadcopter.sdf`. The vehicle is the Open Robotics X3 mass and rotor layout, with an [[IMU]], [[Magnetometer]], [[Barometer]], and [[GNSS]] added in that file. Headless mode is the reliable one on Docker Desktop. `./run-sim.sh --gui` is the window, when a display exists.

## See also

- [[Software in the loop]]
- [[Rigid-body quadrotor]]
