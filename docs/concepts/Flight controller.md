---
type: concept
module: px4_io
tags:
  - concept
  - px4_io
status: article
---

# Flight controller

A flight controller is the small real-time computer bolted to the airframe. It reads the [[IMU]], the [[GNSS]] receiver, the [[Barometer]], and the [[Magnetometer]], and it sends commands to the [[Electronic speed controller|speed controllers]]. The program that does the stabilizing is the [[Autopilot]]. On hardware this playground is aimed at, that program is [[PX4 Autopilot|PX4]] and the board follows the [[Pixhawk]] standard.

## The problem

The rotors have to be corrected hundreds of times a second. A laptop running a desktop operating system is a poor place for that loop: it can pause to do other work, and a pause of a few tens of milliseconds is enough to tumble a small [[Quadrotor]]. The flight controller exists so the fast loop has a computer that does almost nothing else.

## Background

Hobby boards of the late 2000s ran on 8-bit Arduino-class chips. The Pixhawk line, from about 2013, moved the open designs onto 32-bit microcontrollers with a proper [[IMU]] on the board. That is still the shape of a developer drone: one small board, sensors on it, cables to the motors.

## In this playground

[[Gazebo]] stands in for the board's sensors and motors. The Python process is where you write the law. On a real aircraft the fast rate loop usually moves into firmware on this board. The ROS topics are the seam, not the final 1 kHz path.

## See also

- [[Arming and failsafe]]
- [[Offboard mode]]
- [[EKF2]]
