---
type: concept
module: bridge
tags:
  - concept
  - bridge
status: article
aliases:
  - uXRCE-DDS
  - XRCE-DDS
---

# Micro XRCE-DDS

Micro XRCE-DDS is a protocol from eProsima for computers too small to run a full [[DDS]] stack. A thin client runs on the small computer. An agent runs on a larger one. The agent is a normal DDS participant, so everyone else thinks the small computer is too.

## The problem

A [[Flight controller]] cannot spare the RAM for Fast DDS, and you still want its topics on the [[ROS 2]] graph. A bridge that copies messages in both directions is the usual answer. PX4 used to do that with a custom Fast RTPS bridge. Version 1.14, in 2023, switched to this client-and-agent pair, which ships inside the firmware and does not need a special build.

## In this playground

Not used. The running cable is `ros_gz_bridge` in [[Simulation]]. This protocol is what you would add if a real [[PX4 Autopilot]] flight controller later joined the same ROS graph.

## See also

- [[uORB]]
- [[PX4 IO]]
