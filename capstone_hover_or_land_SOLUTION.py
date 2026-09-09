"""
Programming Track -- CAPSTONE: Hover or Land  (SOLUTION)
==============================================================
Phase 06 tie-in: the suicide burn.

This is the payoff for the whole track. Every earlier challenge built
one ingredient of this script:
  Challenge 1 (First Contact)     -- reading live vessel numbers, functions
  Challenge 2 (Auto-Stage)        -- loops that watch a number and react
  Challenge 3 (Auto-Circularize)  -- coding a manual equation into a function
  Challenge 4 (Vis-Viva Checker)  -- a continuous predict-and-compare loop
  Challenge 5 (Descent Watchdog)  -- watching several numbers at once
  Hover preview (intro scripts)   -- proportional control: react harder
                                      the bigger the error is

Two modes:
  MODE = "HOVER" -- climbs to a fixed altitude and holds it forever.
                    Safer, easier, a good first run before trying LAND.
  MODE = "LAND"  -- a real suicide burn: free-fall, then brake hard at
                    exactly the right altitude, then ease down to a
                    soft touchdown with proportional control.

Run this on an unmanned craft with SAS capability, over open, level
ground, with plenty of fuel margin above what you've predicted you'll
need. Test MODE = "HOVER" on Kerbin first before trying MODE = "LAND"
on Duna for real.
"""

import krpc
import time

MODE = "LAND"   # "HOVER" or "LAND"

conn = krpc.connect(name="Capstone - Hover or Land")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
flight = vessel.flight(body.reference_frame)

g = body.surface_gravity


def burn_start_altitude(v0, a_thrust, g):
    """Phase 06's equation: how high above the surface a suicide burn
    needs to start, given current descent speed v0 (positive number)
    and this engine's thrust acceleration a_thrust."""
    net_decel = a_thrust - g
    return (v0 ** 2) / (2 * net_decel)


def throttle_for_target_speed(target_speed, current_speed, gain=0.15):
    """Proportional control, same idea as the hover preview: throttle
    harder the further current_speed is below (more negative than)
    target_speed. Hovering IS this function with target_speed = 0 --
    landing's final approach is this function with a small negative
    target_speed instead."""
    error = current_speed - target_speed  # positive error = falling too fast
    hover_throttle = g / (vessel.available_thrust / vessel.mass)
    throttle = hover_throttle + gain * error
    return max(0.0, min(1.0, throttle))


# --- Point retrograde using SAS, the same way you'd do it by hand -------
vessel.control.sas = True
time.sleep(0.5)
vessel.control.sas_mode = conn.space_center.SASMode.retrograde

if MODE == "HOVER":
    TARGET_ALTITUDE = 100.0
    print(f"HOVER mode: climbing to {TARGET_ALTITUDE} m and holding.")
    vessel.control.throttle = 0.5
    while flight.surface_altitude < TARGET_ALTITUDE:
        time.sleep(0.1)

    print("Holding -- Ctrl+C to end the script.")
    try:
        while True:
            throttle = throttle_for_target_speed(0.0, flight.vertical_speed)
            vessel.control.throttle = throttle
            print(f"alt={flight.surface_altitude:8,.1f} m  "
                  f"vspeed={flight.vertical_speed:6.2f} m/s  "
                  f"throttle={throttle:4.2f}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped -- take back manual control.")

elif MODE == "LAND":
    print("LAND mode: free-falling until it's time to brake...")
    vessel.control.throttle = 0.0

    # --- Phase 1: free-fall, computing the live burn-start altitude ----
    while True:
        v0 = max(0.0, -flight.vertical_speed)  # descent speed, as a positive number
        a_thrust = vessel.available_thrust / vessel.mass
        h_needed = burn_start_altitude(v0, a_thrust, g)
        altitude = flight.surface_altitude

        print(f"falling: alt={altitude:8,.1f} m  v0={v0:6.1f} m/s  "
              f"burn at {h_needed:7,.1f} m")

        if altitude <= h_needed:
            print("-> burn altitude reached, throttling up.")
            break
        time.sleep(0.2)

    # --- Phase 2: hard brake until slow and close to the ground --------
    vessel.control.throttle = 1.0
    while flight.vertical_speed < -5 and flight.surface_altitude > 15:
        print(f"braking: alt={flight.surface_altitude:8,.1f} m  "
              f"vspeed={flight.vertical_speed:6.1f} m/s")
        time.sleep(0.1)

    # --- Phase 3: ease the last few meters down with proportional control
    print("-> final approach, easing down...")
    while (flight.surface_altitude > 0.5
           and vessel.situation != conn.space_center.VesselSituation.landed):
        throttle = throttle_for_target_speed(-1.5, flight.vertical_speed, gain=0.2)
        vessel.control.throttle = throttle
        print(f"final: alt={flight.surface_altitude:7,.1f} m  "
              f"vspeed={flight.vertical_speed:6.2f} m/s  throttle={throttle:4.2f}")
        time.sleep(0.1)

    vessel.control.throttle = 0.0
    print("\nThrottle cut -- check the game to confirm touchdown.")
