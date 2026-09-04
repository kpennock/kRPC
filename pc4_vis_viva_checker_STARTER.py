"""
Programming Track -- Challenge 4: Vis-Viva Live-Checker  (STARTER)
========================================================================
Phase 03 tie-in: the vis-viva equation and conservation of energy.

New ideas: a function with three parameters, a continuous
predict-and-compare loop.

Run this while coasting on an ellipse -- NOT while the engine is
firing, since vis-viva only holds on an unpowered orbit.
"""

import krpc
import time
import math

conn = krpc.connect(name="PC4 - Vis-Viva Checker")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body


def vis_viva_speed(mu, r, a):
    """
    TODO: return v = sqrt(mu * (2/r - 1/a))   (Phase 03's equation)
    """
    pass  # <-- replace this


mu = body.gravitational_parameter
flight = vessel.flight(vessel.orbital_reference_frame)

print("Streaming predicted vs. measured speed (Ctrl+C to stop)...")
try:
    while True:
        # TODO: pull these two live from kRPC each pass through the loop:
        #   a -> vessel.orbit.semi_major_axis
        #   r -> vessel.orbit.radius  (current distance from body's center)
        a = None
        r = None

        # TODO: call vis_viva_speed() with the right three arguments
        predicted = None

        measured = flight.speed
        print(f"r={r}  predicted={predicted}  measured={measured:.1f}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped.")
