---
type: module
module: playground
tags:
  - module
---

# Flight stack

The earlier split into four ROS nodes is gone. [[Control]] is the one process. Estimation and the mixer are code you add in that package when the hover law needs them. A separate node per loop would put a network delay inside the cascade.

Guidance, the outer loop that picks a route, is still future work. It should be a setpoint publisher, not a rewrite of the inner loops.

## See also

- [[Control]]
- [[Cascade control]]
