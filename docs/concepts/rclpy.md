---
type: concept
module: flight
tags:
  - concept
  - flight
status: article
---

# rclpy

rclpy is the official Python client library for [[ROS 2]]. It wraps the same C layer, `rcl`, that the C++ library `rclcpp` uses, so a Python node speaks the same topics, parameters, and quality-of-service settings as any other node. It has shipped with every ROS 2 release since the first one, Ardent, in 2017. Recent releases, [[ROS 2 Jazzy]] included, add type annotations, so a type checker can follow most of the API.

## The problem

A controller has to publish and subscribe. Writing that against raw DDS is a large job. rclpy gives you a `Node`, callbacks for each subscription, and an executor that runs them, in a language that is quick to change while the control law is still a prototype. The cost is speed: Python is fine at a few hundred hertz, and a fast rate loop on real hardware usually moves to C++ or firmware later.

## In this playground

[[Control]] is one Python package, `drone_control`, with one rclpy node. rclpy and the message packages come from apt, not from PyPI. The project venv is created with system site-packages so it can import them. There is no `package.xml` and no [[colcon]] step; `pip install -e control` is the whole build.

The message packages (`sensor_msgs`, `actuator_msgs`, `geometry_msgs`) have no type information, so mypy treats them as untyped. The controller's own code is checked with `mypy --strict`.

## See also

- [[ROS 2 Jazzy]]
- [[Flight stack]]
