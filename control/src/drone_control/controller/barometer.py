"""Altitude from the barometer."""

SEA_LEVEL_PRESSURE = 101325.0
"""Pascals."""


def air_pressure_to_altitude(pressure: float) -> float:
    """Barometric formula of altitude in meters from air pressure in pascals."""
    return 44330.0 * (1.0 - float((pressure / SEA_LEVEL_PRESSURE) ** 0.190263))
