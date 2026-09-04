"""
Programming Track -- CAPSTONE: Hover or Land  (STARTER)
==============================================================
Phase 06 tie-in: the suicide burn.

Everything from Challenges 1-5 (and the intro Hover Preview script)
comes together here. The setup (SAS orientation, HOVER's climb-and-hold
shell, LAND's three-phase shell) is done for you -- your job is the two
functions and the decision logic inside each phase.

Two modes:
  MODE = "HOVER" -- climbs to a fixed altitude and holds it.
  MODE = "LAND"  -- free-fall, hard brake, soft touchdown.

Get HOVER fully working (and tested on Kerbin) before attempting LAND.
"""

import krpc
import time

MODE = "HOVER"   # start here -- switch to "LAND" once HOVER works

conn = krpc.connect(name="Capstone - Hover or Land")
vessel = conn.space_center.active_vessel
body = vessel.orbit.body
flight = vessel.flight(body.reference_frame)

g = body.surface_gravity


def burn_start_altitude(v0, a_thrust, g):
    """
    TODO (needed for LAND mode): Phase 06's equation --
    h = v0^2 / (2 * (a_thrust - g))
    v0 = current descent speed (positive number), a_thrust = engine's
    thrust acceleration, g = local surface gravity.
    """
    pass  # <-- replace this


def throttle_for_target_speed(target_speed, current_speed, gain=0.15):
    """
    TODO: proportional control, same idea as the Hover Preview script.
      error = current_speed - target_speed
      hover_throttle = g / (vessel.available_thrust / vessel.mass)
      throttle = hover_throttle + gain * error
    Then clamp the result to the 0.0-1.0 range before returning it --
    hint: max(0.0, min(1.0, throttle))
    """
    pass  # <-- replace this


# --- Point retrograde using SAS -----------------------------------------
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
            # TODO: call throttle_for_target_speed() to hold vertical
            # speed at 0.0, set vessel.control.throttle to the result,
            # and print alt / vspeed / throttle each pass (see Challenge
            # 5's print style for a pattern to copy).
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopped -- take back manual control.")

elif MODE == "LAND":
    print("LAND mode: free-falling until it's time to brake...")
    vessel.control.throttle = 0.0

    # --- Phase 1: free-fall until the burn-start altitude is reached ---
    while True:
        # TODO: compute v0 (descent speed, positive number, from
        # -flight.vertical_speed), a_thrust (vessel.available_thrust /
        # vessel.mass), and h_needed (call burn_start_altitude()).
        # Then: if flight.surface_altitude <= h_needed, break out of
        # this loop -- it's time to brake.
        time.sleep(0.2)

    # --- Phase 2: hard brake until slow and close to the ground --------
    vessel.control.throttle = 1.0
    while flight.vertical_speed < -5 and flight.surface_altitude > 15:
        print(f"braking: alt={flight.surface_altitude:8,.1f} m  "
              f"vspeed={flight.vertical_speed:6.1f} m/s")
        time.sleep(0.1)

    # --- Phase 3: ease the last few meters down -------------------------
    print("-> final approach, easing down...")
    while (flight.surface_altitude > 0.5
           and vessel.situation != conn.space_center.VesselSituation.landed):
        # TODO: call throttle_for_target_speed(-1.5, flight.vertical_speed,
        # gain=0.2), set the throttle, print status.
        time.sleep(0.1)

    vessel.control.throttle = 0.0
    print("\nThrottle cut -- check the game to confirm touchdown.")
