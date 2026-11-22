---
type: concept
module: playground
tags:
  - concept
  - playground
status: article
---

# Foxglove

Foxglove Studio is a desktop and browser app for looking at robot data: time series, 3D poses, and images, laid out in panels you keep. The company was founded in 2021 by Adrian Macneil and Roman Shtylman. The viewer grew out of Webviz, which Cruise open-sourced in 2019. In 2024 the Studio application became closed source, with a free tier for individual use. The ROS bridge node this repo runs is still how a [[ROS 2]] graph is exposed to the app.

## The problem

`ros2 topic echo` is a terrible way to see whether a rate error is shrinking. A plot of the signals you publish, next to the simulator, is the working surface for a controller and a filter.

## In this playground

`control/run-foxglove.sh` starts `foxglove_bridge` on port 8765. The Windows app connects to `ws://localhost:8765`. Plot the sensor topics and, once a loop exists, the errors you care about. The simulator runs without it.

## See also

- [[ROS 2]]
- [[Ground control station]]
