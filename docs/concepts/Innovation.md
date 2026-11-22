---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Innovation

The innovation, also called the residual, is the measurement minus what the filter predicted that measurement would be. A [[Kalman filter]] uses it twice: the state is corrected in proportion to it, and its size is checked against the innovation covariance. If the filter is honest, a string of innovations looks like zero-mean noise of that predicted size.

## The problem

A filter can report a tiny covariance while being metres wrong, if it has become overconfident. The covariance alone will not tell you. The innovation will. Too small means you distrust the sensor more than you should, or the state is stuck. Too large means the model is wrong, the sensor glitched, or the covariance is overconfident.

## In this playground

When a filter exists inside [[Control]], publish its innovations and plot them in [[Foxglove]]. There is no second estimate from an autopilot to compare against. The check is whether the innovations look like the noise you claimed.

## See also

- [[Mahalanobis gate]]
- [[Covariance]]
