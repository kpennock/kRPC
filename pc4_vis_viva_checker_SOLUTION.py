"""
Programming Track -- Challenge 4: Vis-Viva Live-Checker  (SOLUTION)
========================================================================
Phase 03 tie-in: the vis-viva equation and conservation of energy.

This one doesn't fly anything -- it builds an instrument instead. While
coasting on an unpowered elliptical orbit, it continuously predicts
your speed from vis-viva and compares it to what kRPC actually
measures, live, the whole way around the orbit.

New ideas: a function with three parameters, a continuous
predict-and-compare loop (checking a prediction over and over, instead
of just once).

Run this while coasting on an ellipse (after an apoapsis-raising burn,
like Design challenge 4) -- NOT while the engine is firing, since
vis-viva only holds on an unpowered orbit.
"""

import krpc
import time
import math

conn = krpc.connect(name="PC4 - Vis-Viva Checker")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body


def vis_viva_speed(mu, r, a):
    """Speed anywhere on an orbit of semi-major axis a, at distance r
    from the body's center: v^2 = mu * (2/r - 1/a)."""
    return math.sqrt(mu * (2 / r - 1 / a))


mu = body.gravitational_parameter
flight = vessel.flight(vessel.orbital_reference_frame)

print("Streaming predicted vs. measured speed (Ctrl+C to stop)...")
print(f"{'r (m)':>12}  {'predicted':>10}  {'measured':>10}  {'diff':>8}")
try:
    while True:
        a = vessel.orbit.semi_major_axis
        r = vessel.orbit.radius  # current distance from the body's center
        predicted = vis_viva_speed(mu, r, a)
        measured = flight.speed
        diff = predicted - measured
        print(f"{r:12,.0f}  {predicted:10,.1f}  {measured:10,.1f}  {diff:8,.2f}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped. A small, steady diff is measurement noise; a diff")
    print("that grows means you're not actually coasting unpowered.")
