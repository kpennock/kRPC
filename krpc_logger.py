"""
krpc_logger.py -- reusable KSP telemetry logger for the mission project series.

Connects to a running KSP + kRPC session and logs vessel state to a CSV at a
fixed rate. Every row is tagged with `mission` / `design` / `trajectory`
labels so many flights can be combined later for comparison --
mission_analysis.py groups rows by exactly these three tags, and every future
project in the series (not just Duna) reuses the same three tags, so it's
worth being consistent about what goes in each one:

  --mission     which experiment this is, e.g. "phase1-staging" or "phase4-transfer"
  --design      which of the 5 rocket variants flew (A-E) -- the "same path,
                different rocket" axis
  --trajectory  which flight profile this rocket flew (e.g. "nominal",
                "shallow-aerobrake", "early-departure") -- the "same rocket,
                different path" axis

A comparison run only ever varies ONE of --design / --trajectory at a time;
holding the other fixed is what makes the comparison fair.

Usage:
    python krpc_logger.py --mission phase1-staging --design B --duration 400
    python krpc_logger.py --mission phase4-transfer --design E --trajectory early-10deg

Stop early any time with Ctrl+C -- the CSV is flushed after every row, so a
partial log is always usable for analysis.
"""
import argparse
import csv
import os
import time

import krpc

FIELDNAMES = [
    "ut", "mission", "design", "trajectory", "body", "body_mu", "body_radius",
    "mass", "thrust", "available_thrust", "isp", "altitude", "speed",
    "vertical_speed", "horizontal_speed", "g_force",
    "pos_x", "pos_y", "pos_z", "vel_x", "vel_y", "vel_z",
    "apoapsis_altitude", "periapsis_altitude", "semi_major_axis", "stage",
]


def build_row(conn, vessel, mission, design, trajectory):
    """One telemetry sample. Position/velocity (pos_x/y/z, vel_x/y/z) are
    logged in the orbited body's non-rotating reference frame so
    mission_analysis.py can compute specific energy and angular momentum
    directly from raw vectors -- the same conservation-law checks used in
    Phase 03 of the curriculum. Those axes are NOT aligned to local
    up/north/east, so don't expect any single vel_x/y/z component to read
    like "vertical speed."

    vertical_speed / horizontal_speed are logged separately, computed in the
    vessel's surface reference frame (kRPC keeps this one aligned to local
    up/north/east as the vessel moves). These two ARE directly
    interpretable: vertical_speed is positive while climbing, negative while
    falling, and crosses zero at apoapsis -- exactly like the navball
    readout, and safe to difference once for a clean accel_vertical."""
    body = vessel.orbit.body
    ref = body.non_rotating_reference_frame
    surface_ref = vessel.surface_reference_frame
    flight = vessel.flight(ref)
    surface_flight = vessel.flight(surface_ref)
    pos = vessel.position(ref)
    vel = vessel.velocity(ref)
    orbit = vessel.orbit
    # vessel.specific_impulse is the combined Isp of the currently active
    # engines (kRPC computes it from their individual Isps and thrusts),
    # already accounting for atmospheric pressure at the vessel's current
    # altitude. It reads 0 when no engine is producing thrust (e.g. coasting).
    return {
        "ut": conn.space_center.ut,
        "mission": mission,
        "design": design,
        "trajectory": trajectory,
        "body": body.name,
        "body_mu": body.gravitational_parameter,
        "body_radius": body.equatorial_radius,
        "mass": vessel.mass,
        "thrust": vessel.thrust,
        "available_thrust": vessel.available_thrust,
        "isp": vessel.specific_impulse,
        "altitude": flight.mean_altitude,
        "speed": flight.speed,
        "vertical_speed": surface_flight.vertical_speed,
        "horizontal_speed": surface_flight.horizontal_speed,
        "g_force": flight.g_force,
        "pos_x": pos[0], "pos_y": pos[1], "pos_z": pos[2],
        "vel_x": vel[0], "vel_y": vel[1], "vel_z": vel[2],
        "apoapsis_altitude": orbit.apoapsis_altitude,
        "periapsis_altitude": orbit.periapsis_altitude,
        "semi_major_axis": orbit.semi_major_axis,
        "stage": vessel.control.current_stage,
    }


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--mission", required=True, help='experiment tag, e.g. "phase1-staging"')
    parser.add_argument("--design", default="A", help="rocket-design label A-E (default A)")
    parser.add_argument("--trajectory", default="nominal", help="flight-profile label (default nominal)")
    parser.add_argument("--rate", type=float, default=2.0, help="samples per second (default 2)")
    parser.add_argument("--duration", type=float, default=None, help="stop after N seconds (default: run until Ctrl+C)")
    parser.add_argument("--outdir", default="logs", help="folder to write the CSV into (default ./logs)")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    outpath = os.path.join(args.outdir, f"{args.mission}_{args.design}_{args.trajectory}.csv")

    conn = krpc.connect(name="telemetry-logger")
    vessel = conn.space_center.active_vessel

    print(f"Connected. Logging '{args.mission}' (design={args.design}, trajectory={args.trajectory})")
    print(f"Writing to {outpath} at {args.rate} Hz -- Ctrl+C to stop early.")

    start = time.time()
    rows_written = 0
    with open(outpath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        try:
            while args.duration is None or (time.time() - start) < args.duration:
                row = build_row(conn, vessel, args.mission, args.design, args.trajectory)
                writer.writerow(row)
                f.flush()
                rows_written += 1
                time.sleep(1.0 / args.rate)
        except KeyboardInterrupt:
            print("\nStopped by user.")

    print(f"Wrote {rows_written} rows to {outpath}")


if __name__ == "__main__":
    main()
