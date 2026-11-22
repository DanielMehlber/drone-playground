---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Magnetometer

A magnetometer measures the local magnetic field, which on Earth points roughly along magnetic north. A three-axis chip is an electronic compass. Paired with the [[IMU]], it is how a [[Quadrotor]] learns which way is north when [[GNSS]] velocity is too small to show a heading.

## The problem

Gyros drift in yaw. Without a heading reference the aircraft slowly spins its idea of north. The magnetic field is that reference, and it is a bad one near motors, battery wires, and rebar. Current in the power cables makes a field the sensor cannot tell from the Earth's.

## Background

The compass is ancient. Three-axis electronic sensors arrived on flight boards with the MEMS [[IMU]] generation around 2010. Calibration, waving the aircraft in the air before flight, is still a normal preflight step on a real [[Pixhawk]].

## In this playground

`/magnetometer` is the field in body forward-left-up, in tesla. Use it as a heading update after attitude from the accelerometer already works. A wrong magnetic calibration looks like a yaw that never settles.

## See also

- [[Extended Kalman filter]]
- [[Coordinate frames]]
