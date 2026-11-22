---
type: concept
module: control
tags:
  - concept
  - control
status: article
---

# Wrench

A wrench is a force and a torque together. The word is from classical mechanics, the combined push and twist on a rigid body. Force is in newtons. Torque is in newton-metres. On a [[Quadrotor]] the useful wrench is expressed in the body frame: thrust along up, and torques about forward, left, and up.

## The problem

[[Control]] wants to say "push this hard and twist this hard." The motors want four speeds. Those are different languages. The wrench is the language of the loops. [[Control allocation]] translates it.

## In this playground

A wrench is an internal value in [[Control]], body forward-left-up. The topic the plant listens to is four rotor speeds, not the wrench. A zero wrench is a real decision to fall. The stub publishes no speeds until a loop exists.

## See also

- [[Rigid-body quadrotor]]
- [[PID control]]
