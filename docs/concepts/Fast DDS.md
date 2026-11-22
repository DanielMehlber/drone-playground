---
type: concept
module: bridge
tags:
  - concept
  - bridge
status: article
---

# Fast DDS

Fast DDS is eProsima's implementation of [[DDS]], and the default one inside [[ROS 2 Jazzy]]. The project started as Fast RTPS in the mid-2010s. It took the Fast DDS name around 2019, when it grew the standard DDS programming interface and not only the RTPS wire protocol underneath.

## The problem

DDS is a paper standard. Something has to send the UDP packets. ROS 2 vendors one implementation so a default install works, and lets you swap it. Swapping it inside this repo would mean a different discovery setup, so we stay on the default.

## In this playground

The default profile is enough. In the dev container every process is on one host. In the Compose deployment the containers share one Docker network, and Fast DDS finds them by multicast. If `ros2 topic list` is empty across containers, check that `ROS_DOMAIN_ID` matches and that the containers are on the same network. A participant profile with fixed peers, pointed to by `FASTRTPS_DEFAULT_PROFILES_FILE`, is the fallback when multicast is blocked. Every peer hostname in it must resolve when the process starts, or Fast DDS ignores the whole file.

## See also

- [[Micro XRCE-DDS]]
- [[Dev containers]]
