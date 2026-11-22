---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
aliases:
  - GPS
---

# GNSS

GNSS means global navigation satellite system. Receivers listen to several satellites and solve for position, and usually velocity, on the Earth. GPS is the United States system: the first satellite flew in 1978 and the constellation was declared operational in 1995. GLONASS, Galileo, and BeiDou are the Russian, European, and Chinese systems. A chip that uses more than one of them is a GNSS receiver. People still say GPS for the whole idea.

## The problem

Integrating an [[IMU]] drifts. A satellite fix pulls the position back, a few times a second, with an error of roughly a metre for a cheap receiver and much less for a survey receiver. The fix is slow, jumpy, and absent indoors. The filter's job is to trust it when it is honest and ignore it when it is not. See [[Mahalanobis gate]].

## In this playground

`/navsat` is `sensor_msgs/NavSatFix`: latitude, longitude, and altitude. The world origin is in the SDF. Treat the fix as an update, not as the state. It is slow and about a metre. It is the wrong sensor for the rate loop.

## See also

- [[Barometer]]
- [[Kalman filter]]
