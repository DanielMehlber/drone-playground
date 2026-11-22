---
type: concept
module: simulation
tags:
  - concept
  - simulation
status: article
---

# Rigid-body quadrotor

The model [[Gazebo]] integrates for this aircraft is a rigid body: one mass, one inertia, no flexing arms. Gravity pulls in the world. Each rotor adds a force along body up and a torque from its thrust times its lever arm, plus a small torque from how hard it is spinning. The equations are Newton's second law for translation and Euler's equation for rotation. Textbooks have written them this way for quadrotors since the research wave of the 2000s. The rigid-body laws themselves are centuries old.

## The problem

If you also invent the integrator, you are doing numerical physics, not control. [[Gazebo]] already integrates this model. Your job is to pick the four rotor speeds that produce the force and the torque.

## What changes the numbers

Mass sets the hover thrust: weight divided by four, before you account for tilt. Inertia sets how fast a torque becomes a rate. Wrong mass looks like a throttle bias. Wrong inertia looks like a rate gain that is too hot or too dull. Change those in the model when a loop works on the default aircraft and you want to see it fail.

## See also

- [[Motor model]]
- [[Wrench]]
- [[Quadrotor]]
