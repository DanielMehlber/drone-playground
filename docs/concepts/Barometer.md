---
type: concept
module: estimation
tags:
  - concept
  - estimation
status: article
---

# Barometer

A barometer measures air pressure. Pressure falls as you climb, so a calibration turns pressure into a height above a reference. Aircraft have used pressure altitude for as long as they have had instruments. The chip on a [[Flight controller]] is a MEMS sensor, standard on open boards since the early 2010s.

## The problem

[[GNSS]] altitude is often noisier than horizontal position. A barometer is a cheap, fast second opinion on height. Wind, weather, and the blast from your own rotors move the reading, so it is an aid, not a ruler.

## In this playground

`/air_pressure` is `sensor_msgs/FluidPressure`, in pascals. Height comes from converting pressure yourself. That conversion is the first altitude signal for hover, before you trust [[GNSS]] vertically.

## See also

- [[GNSS]]
- [[Sensor noise]]
