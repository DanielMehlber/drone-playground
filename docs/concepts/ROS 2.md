---
type: concept
module: interfaces
tags:
  - concept
  - interfaces
status: article
aliases:
  - ROS
---

# ROS 2

ROS 2 is a set of libraries and tools for writing robot programs as separate processes that exchange typed messages. A process is a node. A named stream of messages is a topic. The messages are defined in text files and compiled into code. The current transport underneath is [[DDS]].

## The problem

A filter, a controller, a simulator, and a plotter need to share data without becoming one program. They also need to restart independently when one of them crashes. ROS is the common way to do that in robotics labs, which is why drivers and tutorials already exist for it.

## Background

Willow Garage started ROS in 2007. The first boxed release, Box Turtle, was 2010. That generation, ROS 1, was a research system with a central master process. ROS 2 was begun in 2014 so the same idea could run on real products: no single master, DDS underneath, and support for more than Ubuntu on a laptop. The first ROS 2 release, Ardent, was December 2017. ROS 1's last Ubuntu release, Noetic, reached end of life in May 2025. New work belongs on ROS 2.

## In this playground

[[ROS 2 Jazzy]] is the cable. Gazebo sits behind `ros_gz_bridge`. [[Control]] is one Python node via [[rclpy]]. The messages are the standard sensor and actuator types. There is no custom package and no [[colcon]] step.

## See also

- [[REP-103]]
- [[Companion computer]]
