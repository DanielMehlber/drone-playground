---
type: concept
module: bridge
tags:
  - concept
  - bridge
status: article
aliases:
  - DDS discovery
---

# DDS

DDS, the Data Distribution Service, is a standard for programs on different machines to publish and subscribe to data without calling each other directly. The Object Management Group adopted version 1.0 in December 2004. It came from real-time industries, including defense and industrial control, where a late sample is a fault. [[ROS 2]] uses DDS as its transport.

## The problem

A simulator, an autopilot, and a controller need a shared stream of typed samples. A single "master" process that introduces them, which is what ROS 1 did, is an extra thing to crash. DDS lets each program announce itself and find the others.

That search is discovery. On one computer it is usually multicast. The dev container is one computer. The Compose deployment puts its containers on one Docker network, where multicast reaches them too. `ROS_DOMAIN_ID` is pinned to 83 so we do not collide with another ROS on the same machine. See [[Fast DDS]] for the fallback when multicast is blocked.

## In this playground

[[Fast DDS]] is the implementation inside [[ROS 2 Jazzy]]. The sim container and the control container find each other with it. [[Micro XRCE-DDS]] is the smaller cousin that lets a [[PX4 Autopilot]] join a graph like this one. It is not running here.

## See also

- [[Bridge]]
- [[uORB]]
