"""
Phase 01/02 kRPC Intro -- Script 3: Auto-circularize
======================================================
Goal: put Phase 02's equation to work. Instead of eyeballing when to cut
the engine, this script waits for apoapsis, points the rocket prograde,
and burns until the orbit is (approximately) circular -- using the
exact v = sqrt(mu/r) equation from the manual to know what "circular"
even means at this altitude, computed live instead of read off a table.

Assumes: you've already launched and have an ascending trajectory with
an apoapsis set above the atmosphere (roughly 70+ km at Kerbin). This
script does not launch or stage for you -- combine it with Script 2 if
you want the whole ascent automated end to end.

Heads up: this uses a fixed full-throttle burn and stops the moment
periapsis reaches the target, which is simple but not precise -- a
high-thrust engine will overshoot a little. (Good discussion question
for class: why does that overshoot happen, and what would fix it?
Throttling down as you get close is the real answer, and it's exactly
the kind of adjustment Script 4's proportional-control idea is built
around.)
"""

import krpc
import time
import math

conn = krpc.connect(name="03 - Auto Circularize")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body

# ---------------------------------------------------------------------
# Step 1: wait for apoapsis. vessel.orbit.time_to_apoapsis is a live
# number that counts down -- we just poll it until it's small.
# ---------------------------------------------------------------------
print("Coasting to apoapsis...")
while vessel.orbit.time_to_apoapsis > 15:
    print(f"  time to apoapsis: {vessel.orbit.time_to_apoapsis:6.1f} s")
    time.sleep(1)

# ---------------------------------------------------------------------
# Step 2: point prograde. The autopilot needs a reference frame -- we
# use the vessel's ORBITAL reference frame so "prograde" means "the
# direction of orbital motion," not "wherever the nose happens to be
# pointing relative to the ground."
# ---------------------------------------------------------------------
print("Orienting prograde...")
vessel.auto_pilot.reference_frame = vessel.orbital_reference_frame
vessel.auto_pilot.target_direction = (0, 1, 0)  # prograde, in this frame
vessel.auto_pilot.engage()
vessel.auto_pilot.wait()

# ---------------------------------------------------------------------
# Step 3: the actual physics. This is Phase 02's circular-velocity
# equation, coded directly -- not looked up, computed live from the
# vessel's own current orbit.
# ---------------------------------------------------------------------
mu = body.gravitational_parameter
r = vessel.orbit.apoapsis  # distance from the body's CENTER at apoapsis (meters)

v_circular = math.sqrt(mu / r)  # <-- straight out of Phase 02: v = sqrt(mu / r)

flight_orbital = vessel.flight(vessel.orbital_reference_frame)
v_current = flight_orbital.speed

dv_needed = v_circular - v_current
print(f"\nAt apoapsis (r = {r:,.0f} m from {body.name}'s center):")
print(f"  current speed:   {v_current:,.1f} m/s")
print(f"  circular speed:  {v_circular:,.1f} m/s   <- v = sqrt(mu / r)")
print(f"  dv needed:       {dv_needed:,.1f} m/s")

# ---------------------------------------------------------------------
# Step 4: burn until periapsis has risen to meet apoapsis -- that's
# what "circular" actually means, and it's a more reliable stop
# condition than trying to time a fixed-length burn from a Δv number.
# ---------------------------------------------------------------------
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
print(f"  predicted circular speed was {v_circular:,.1f} m/s -- ")
print(f"  compare that to what KER shows now and see how close the")
print(f"  hand-coded equation actually got.")
