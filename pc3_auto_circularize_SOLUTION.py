"""
Programming Track -- Challenge 3: Auto-Circularize  (SOLUTION)
===================================================================
Phase 02 tie-in: circular orbital velocity.

New ideas: writing a function around a real physics equation, pointing
the autopilot in an orbital direction (prograde), and a precise
"stop when a condition is met" loop instead of a fixed-length burn.
"""

import krpc
import time
import math

conn = krpc.connect(name="PC3 - Auto Circularize")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body

print("Coasting to apoapsis...")
while vessel.orbit.time_to_apoapsis > 15:
    print(f"  time to apoapsis: {vessel.orbit.time_to_apoapsis:6.1f} s")
    time.sleep(1)

print("Orienting prograde...")
vessel.auto_pilot.reference_frame = vessel.orbital_reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)  # prograde in this frame
vessel.auto_pilot.engage()
vessel.auto_pilot.wait()


def circular_velocity(mu, r):
    """Phase 02's equation: v = sqrt(mu / r)."""
    return math.sqrt(mu / r)


mu = body.gravitational_parameter
r = vessel.orbit.apoapsis  # distance from body's center at apoapsis

v_circular = circular_velocity(mu, r)

flight_orbital = vessel.flight(vessel.orbital_reference_frame)
v_current = flight_orbital.speed

print(f"\nAt apoapsis (r = {r:,.0f} m):")
print(f"  current speed:   {v_current:,.1f} m/s")
print(f"  circular speed:  {v_circular:,.1f} m/s   <- circular_velocity(mu, r)")

target_periapsis = vessel.orbit.apoapsis_altitude
print(f"\nBurning until periapsis reaches {target_periapsis:,.0f} m...")

vessel.control.throttle = 1.0
while vessel.orbit.periapsis_altitude < target_periapsis:
    print(f"  periapsis: {vessel.orbit.periapsis_altitude:9,.0f} m   "
          f"(target {target_periapsis:,.0f} m)")
    time.sleep(0.2)

vessel.control.throttle = 0.0
vessel.auto_pilot.disengage()

print("\nCircularization burn complete.")
print(f"  final periapsis: {vessel.orbit.periapsis_altitude:,.0f} m")
print(f"  final apoapsis:  {vessel.orbit.apoapsis_altitude:,.0f} m")
