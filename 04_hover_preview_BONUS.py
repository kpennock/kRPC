"""
Phase 01/02 kRPC Intro -- Script 4 (BONUS / preview, not core): Hover
=======================================================================
This one's a preview, not part of the required Phase 01/02 sequence --
a taste of where this is all heading. Phase 06 will build a real Duna
hover-and-landing autopilot; this is the simplest possible version of
the same idea, flown safely over the launchpad at Kerbin, so you can
see the shape of the code before the real thing gets harder (weaker
gravity, no convenient flat pad, an actual descent to manage instead of
just holding still).

Run this on an unmanned test craft with plenty of fuel, over open
ground, with nothing else nearby. It will fly to ~100 m and hover
there until you interrupt it (Ctrl+C).

The idea: a "P controller" (proportional controller) -- an extremely
common piece of real engineering, used in everything from cruise
control to drone flight controllers. The rule is almost embarrassingly
simple:
  * measure the error -- how far off you are from the target
  * push proportionally harder the bigger that error is
  * measure again, many times per second, and repeat

No trigonometry, no rocket equation -- just watch a number, react a
little, watch again.
"""

import krpc
import time

conn = krpc.connect(name="04 - Hover Preview")
vessel = conn.space_center.active_vessel

TARGET_ALTITUDE = 100.0   # meters above the launchpad
ALTITUDE_GAIN = 0.05      # how hard to react to 1 m of altitude error -- tune this
SPEED_GAIN = 0.10         # how hard to react to vertical speed -- this is what
                          # keeps the hover from oscillating (see note below)

flight = vessel.flight(vessel.orbit.body.reference_frame)
vessel.control.sas = True

print("Getting off the pad...")
vessel.control.throttle = 0.5
while flight.mean_altitude < TARGET_ALTITUDE:
    time.sleep(0.1)

print(f"Holding {TARGET_ALTITUDE:.0f} m -- Ctrl+C to end the script.")
try:
    while True:
        error = TARGET_ALTITUDE - flight.mean_altitude
        vertical_speed = flight.vertical_speed

        # This throttle rule reacts to BOTH the altitude error and the
        # current vertical speed. Reacting to altitude error alone
        # (a plain "P controller") tends to overshoot and oscillate --
        # push up, fly past the target, push down, fly past it the
        # other way, forever. Subtracting a term proportional to
        # vertical_speed damps that out: it's reacting not just to
        # "how far off am I" but to "how fast am I already moving,"
        # which is exactly the extra idea a full PID controller
        # (Phase 06) builds further on.
        throttle = 0.5 + ALTITUDE_GAIN * error - SPEED_GAIN * vertical_speed
        vessel.control.throttle = max(0.0, min(1.0, throttle))

        print(f"  alt={flight.mean_altitude:7.1f} m   "
              f"v_speed={vertical_speed:6.1f} m/s   "
              f"throttle={vessel.control.throttle:4.2f}")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nStopped -- throttle left as last set, take back manual control.")
