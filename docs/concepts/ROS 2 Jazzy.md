---
type: concept
module: interfaces
tags:
  - concept
  - interfaces
status: article
aliases:
  - Jazzy
---

# ROS 2 Jazzy

Jazzy Jalisco is a long-term support distribution of [[ROS 2]]. It was released on 23 May 2024 and is supported until May 2029. The name follows the project's habit of alphabetical turtle names. Jazzy is the tenth ROS 2 distribution. Its usual desktop is Ubuntu 24.04.

## The problem

ROS is a moving set of packages. If every library picks a different snapshot, nothing builds. A distribution is a freeze: these package versions, this Ubuntu, this support window. Projects pin one.

## In this playground

One Dockerfile, `docker/Dockerfile`, has Jazzy and Gazebo Harmonic. Harmonic is the Gazebo release Jazzy expects. The Humble bridge against Harmonic is a known mismatch, so this repo stays on Jazzy. [[rclpy]] and the message packages come from this install, not from PyPI.

## See also

- [[colcon]]
- [[Fast DDS]]
