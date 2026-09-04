"""
Programming Track -- Challenge 3: Auto-Circularize  (STARTER)
===================================================================
Phase 02 tie-in: circular orbital velocity.

New ideas: writing a function around a real physics equation, pointing
the autopilot prograde, and a precise stop-when-condition-met loop.

Fill in the TODOs. The coast-to-apoapsis and prograde-orientation parts
are done for you -- this challenge is about the physics function and
the burn loop.
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
    """
    TODO: return v = sqrt(mu / r)  (Phase 02's equation)
    import math is already done above -- use math.sqrt()
    """
    pass  # <-- replace this


mu = body.gravitational_parameter
r = vessel.orbit.apoapsis  # distance from body's center at apoapsis

# TODO: call circular_velocity() with the right two arguments
v_circular = None

flight_orbital = vessel.flight(vessel.orbital_reference_frame)
v_current = flight_orbital.speed
print(f"\ncurrent speed: {v_current:.1f} m/s   target: {v_circular}")

target_periapsis = vessel.orbit.apoapsis_altitude
vessel.control.throttle = 1.0

# TODO: write a while loop that keeps the throttle open until
# vessel.orbit.periapsis_altitude reaches target_periapsis, printing
# progress on each pass (same pattern as Challenge 2's loop). Then set
# throttle back to 0.0 and call vessel.auto_pilot.disengage().

print("\nDone -- check final periapsis/apoapsis against your prediction.")
