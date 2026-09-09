"""
Programming Track -- Challenge 5: Descent Watchdog  (SOLUTION)
====================================================================
Phase 05 tie-in: aerobraking, and the crew-safety g-limit idea that
comes back in Phase 07.

A monitoring script, not a control script -- it doesn't fly anything,
it watches several numbers at once and warns you the instant one
crosses a safety limit you set. Run it during an aerobraking pass or a
reentry.

New ideas: watching multiple streams/values at once, and a running
list that collects readings over time so you can report the worst one
at the end.
"""

import krpc
import time

conn = krpc.connect(name="PC5 - Descent Watchdog")
vessel = conn.space_center.active_vessel
flight = vessel.flight(vessel.orbit.body.reference_frame)

G_FORCE_LIMIT = 8.0      # set your own crew-safety limit, in g's
ALTITUDE_WARN = 5000.0   # meters -- warn if still descending fast this low

g_force_log = []  # every g-force reading we've seen gets appended here

print("Watching descent (Ctrl+C to stop)...")
try:
    while True:
        g_force = flight.g_force
        altitude = flight.mean_altitude
        vertical_speed = flight.vertical_speed

        g_force_log.append(g_force)

        status = ""
        if g_force > G_FORCE_LIMIT:
            status += f"  !! G-FORCE LIMIT EXCEEDED ({g_force:.1f}g > {G_FORCE_LIMIT}g)"
        if altitude < ALTITUDE_WARN and vertical_speed < -100:
            status += f"  !! FAST AND LOW ({vertical_speed:.0f} m/s at {altitude:,.0f} m)"

        print(f"alt={altitude:9,.0f} m  vspeed={vertical_speed:7.1f} m/s  "
              f"g={g_force:4.1f}{status}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print(f"\nStopped. Max g-force seen this pass: {max(g_force_log):.1f}g "
          f"(over {len(g_force_log)} readings).")
