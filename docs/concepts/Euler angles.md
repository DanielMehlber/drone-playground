---
type: concept
module: control
tags:
  - concept
  - control
status: article
---

# Euler angles

Euler angles are three angles, roll, pitch, and yaw, that describe a rotation. Leonhard Euler introduced this way of composing rotations in the eighteenth century, around 1776. They are the angles a person means by "tilted a bit and turned left."

## The problem

They are a good display and a bad state. The order of the three rotations matters, and at a steep pitch the roll and yaw axes line up, which is gimbal lock. A [[PID control|PID]] written on Euler angles then commands nonsense. [[Quaternion]] attitude avoids that. Ground stations still show Euler angles because people can read them.

## In this playground

Use Euler angles in [[Foxglove]] when you want to see a tilt. Keep the filter state and the [[Geometric attitude control|attitude controller]] on quaternions. A small-angle Euler error is a fair approximation while the aircraft is near hover, which is why a first [[Cascade control|cascade]] often starts there and then gets replaced.

## See also

- [[Coordinate frames]]
- [[Cascade control]]
