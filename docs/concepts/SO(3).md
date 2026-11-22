---
type: concept
module: control
tags:
  - concept
  - control
status: article
aliases:
  - SE(3)
---

# SO(3)

SO(3) is the set of all rotations in three-dimensional space. Each member can be written as a 3×3 matrix that preserves lengths and has determinant 1, or as a unit [[Quaternion]]. The name is from the nineteenth-century classification of continuous groups: "special orthogonal group of dimension 3." Sophus Lie's work in the 1870s and 1880s is the mathematical background. SE(3) is the same idea with translation added, a rotation plus a shift. A rigid aircraft's pose lives in SE(3). Its attitude alone lives in SO(3).

## The problem

[[Euler angles]] are three numbers with seams. Saying a controller works "on SO(3)" means the error it uses is a rotation in this set, so the math does not depend on which chart you picked. The quadrotor paper people cite, Lee, Leok, and McClamroch, 2010, has SE(3) in the title because it tracks a full pose, not only a tilt.

## In this playground

You do not need to implement matrix groups. You need to know why [[Geometric attitude control]] refuses to subtract Euler angles. Store attitude as a quaternion. The error is the rotation that takes the current attitude onto the desired one.

## See also

- [[Quaternion]]
- [[Geometric attitude control]]
