---
type: concept
module: control
tags:
  - concept
  - control
status: article
aliases:
  - INDI
---

# Incremental nonlinear dynamic inversion

Incremental nonlinear dynamic inversion, INDI, commands a change in actuator position from a change in acceleration you want, using a measurement of the current acceleration instead of a full model of the forces. The aircraft paper most often cited is Sieberling, Chu, and Mulder, 2010. Multirotor papers followed in the mid-2010s, including work by Ewoud Smeur and colleagues around 2016. [[PX4 Autopilot|PX4]] offers an INDI option on the rate loop for aggressive flight.

## The problem

A model-based inverse needs mass, inertia, and a thrust curve, and those are wrong as soon as the battery sags or the propellers get dirty. Incrementing from the measured angular acceleration cancels a lot of that error, because the unknown force is already in the measurement. The cost is that you need a clean, fast acceleration signal, which means filtering the gyro without adding too much delay.

## In this playground

Treat it as a replacement for the rate [[PID control|PID]] inside [[Control]], after that PID already hovers. Compare the two on the same four rotor speeds and the same aircraft. If INDI is better only because the filter was retuned, the experiment is not finished.

## See also

- [[Sensor noise]]
- [[Motor model]]
