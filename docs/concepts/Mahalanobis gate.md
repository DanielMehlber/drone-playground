---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Mahalanobis gate

A Mahalanobis gate rejects a measurement whose [[Innovation]] is too large for the [[Covariance]] the filter predicted. The distance was defined by Prasanta Chandra Mahalanobis in 1936. Unlike a plain Euclidean distance, it scales each axis by how uncertain that axis is, and it accounts for axes that vary together. A gate is a threshold on that distance: above it, skip the update.

## The problem

One bad [[GNSS]] jump will drag a [[Kalman filter]] off the trajectory, and the filter will then spend seconds believing the mistake. A threshold in metres is wrong because a metre is huge in hover and small at speed, and because the filter's own doubt changes. The Mahalanobis distance is the threshold in the filter's units.

## In this playground

When a filter exists in [[Control]], put the test on the GNSS update first. Log rejected samples. A gate that rejects everything means R is too small or the predict step is lost. A gate that never fires is not a test.

## See also

- [[Innovation]]
- [[GNSS]]
