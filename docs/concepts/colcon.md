---
type: concept
module: interfaces
tags:
  - concept
  - interfaces
status: article
---

# colcon

colcon is the build tool [[ROS 2]] uses to compile a workspace of packages in the right order. It appeared around 2018, replacing catkin from ROS 1. You point it at folders that contain a `package.xml`, and it produces an `install` tree you source from a shell.

## The problem

A message package must be compiled before a node that uses those messages. Doing that by hand, and remembering which shell variables point at the result, is how workspaces break. colcon encodes the order and writes one `setup.bash`.

## In this playground

This repo does not run colcon. The controller uses messages that already ship with [[ROS 2 Jazzy]], and it is a plain Python package installed with pip, using [[rclpy]] from the ROS install. Colcon is how you would build a custom message package if you later add one.

## See also

- [[ROS 2 Jazzy]]
- [[Interfaces]]
