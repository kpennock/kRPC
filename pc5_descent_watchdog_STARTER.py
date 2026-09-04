"""
Programming Track -- Challenge 5: Descent Watchdog  (STARTER)
====================================================================
Phase 05 tie-in: aerobraking, and the crew-safety g-limit idea that
comes back in Phase 07.

New ideas: watching multiple values at once, and a running list that
collects readings over time.

Fill in the TODOs. Run this during an aerobraking pass or a reentry.
"""

import krpc
import time

conn = krpc.connect(name="PC5 - Descent Watchdog")
vessel = conn.space_center.active_vessel
flight = vessel.flight(vessel.orbit.body.reference_frame)

G_FORCE_LIMIT = 8.0      # set your own crew-safety limit, in g's
ALTITUDE_WARN = 5000.0   # meters -- warn if still descending fast this low

g_force_log = []  # TODO: append each g-force reading to this list, below

print("Watching descent (Ctrl+C to stop)...")
try:
    while True:
        # TODO: read these three live from `flight`:
        #   g_force        -> flight.g_force
        #   altitude       -> flight.mean_altitude
        #   vertical_speed -> flight.vertical_speed
        g_force = None
        altitude = None
        vertical_speed = None

        # TODO: append g_force to g_force_log

        status = ""
        # TODO: build the warning string.
        #   if g_force > G_FORCE_LIMIT: add a "G-FORCE LIMIT EXCEEDED" message
        #   if altitude < ALTITUDE_WARN and vertical_speed < -100: add a
        #     "FAST AND LOW" message
        # (both can be true at once -- that's why status starts as "" and
        # gets += on each check, rather than using elif)

        print(f"alt={altitude}  vspeed={vertical_speed}  g={g_force}{status}")
        time.sleep(0.5)
except KeyboardInterrupt:
    # TODO: print the max value in g_force_log, and how many readings
    # were collected. Hints: max(g_force_log), len(g_force_log)
    print("\nStopped.")
