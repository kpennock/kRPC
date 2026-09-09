import csv
import os
import time
import krpc

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
SAMPLE_RATE_HZ = 5.0  # 5 samples per second (0.2s interval)
SLEEP_INTERVAL = 1.0 / SAMPLE_RATE_HZ

# A vessel counts as having reached LKO once both apoapsis and periapsis
# stay above this altitude (meters). 70,000 m is just above Kerbin's
# atmosphere -- adjust if your target orbit is different.
LKO_ALTITUDE_THRESHOLD_M = 70000

COMPARISON_FILENAME = "rocket_comparison.csv"

# ---------------------------------------------------------------------------
# Connect to KSP
# ---------------------------------------------------------------------------
print("Connecting to Kerbal Space Program via kRPC...")

try:
    print("Attempting to connect to kRPC...")
    conn = krpc.connect(
        name='Data Logger',
        address='127.0.0.1',  # If this fails, try '0.0.0.0' or 'localhost'
        rpc_port=50000,
        stream_port=50001
    )
    vessel = conn.space_center.active_vessel
    print(f"Successfully connected to KSP! Vessel: {vessel.name}")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

body = vessel.orbit.body

# Name this rocket configuration -- used for the per-flight CSV filename
# and as the label in the cross-config comparison chart.
config_name = input(
    "Enter a name for this rocket configuration (e.g. 'ThreeStage_HeavyPayload'): "
).strip()
if not config_name:
    config_name = f"config_{time.strftime('%Y%m%d_%H%M%S')}"

LOG_FILENAME = f"flight_telemetry_{config_name}.csv"

# Flight frame references
flight_surface = vessel.flight(vessel.surface_reference_frame)
flight_orbital = vessel.flight(vessel.orbital_reference_frame)

print(f"Setting up telemetry data streams for '{config_name}'...")

# ---------------------------------------------------------------------------
# Streams
# ---------------------------------------------------------------------------
ut_stream = conn.add_stream(getattr, conn.space_center, "ut")
alt_stream = conn.add_stream(getattr, flight_surface, "mean_altitude")
surf_speed_stream = conn.add_stream(getattr, flight_surface, "speed")
vertical_speed_stream = conn.add_stream(getattr, flight_surface, "vertical_speed")
horizontal_speed_stream = conn.add_stream(getattr, flight_surface, "horizontal_speed")
orbit_speed_stream = conn.add_stream(getattr, flight_orbital, "speed")
pitch_stream = conn.add_stream(getattr, flight_surface, "pitch")
dynamic_pressure_stream = conn.add_stream(getattr, flight_surface, "dynamic_pressure")
mass_stream = conn.add_stream(getattr, vessel, "mass")
thrust_stream = conn.add_stream(getattr, vessel, "thrust")
isp_stream = conn.add_stream(getattr, vessel, "specific_impulse")
# vessel.delta_v is a plain float: current stage's delta-v under current
# atmospheric conditions. There's no single "total across all stages" RPC,
# so that's recomputed each loop iteration by summing vessel.stages.
stage_dv_stream = conn.add_stream(getattr, vessel, "delta_v")
apoapsis_stream = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
periapsis_stream = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")

headers = [
    "mission_time_s",
    "altitude_m",
    "surface_speed_ms",
    "orbital_speed_ms",
    "vertical_speed_ms",
    "horizontal_speed_ms",
    "pitch_deg",
    "dynamic_pressure_pa",
    "total_mass_kg",
    "thrust_kn",
    "twr",
    "isp_s",
    "current_stage_deltav_ms",
    "total_remaining_deltav_ms",
    "apoapsis_m",
    "periapsis_m",
]

start_ut = ut_stream()

# Tracked across the whole flight, used for the comparison-file summary
initial_total_dv = None
peak_dynamic_pressure = 0.0
peak_twr = 0.0
lko_summary = None  # filled in the first moment LKO conditions are met

print(f"Starting flight recording to '{LOG_FILENAME}' at {SAMPLE_RATE_HZ} Hz.")
print("Press Ctrl+C once you've circularized in LKO (or to stop early).")

with open(LOG_FILENAME, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)

    try:
        while True:
            current_ut = ut_stream()
            mission_time = current_ut - start_ut

            altitude = alt_stream()
            surf_speed = surf_speed_stream()
            orb_speed = orbit_speed_stream()
            v_speed = vertical_speed_stream()
            h_speed = horizontal_speed_stream()
            pitch = pitch_stream()
            dyn_q = dynamic_pressure_stream()
            total_mass = mass_stream()  # Metric tons
            thrust_n = thrust_stream()  # Newtons
            thrust_kn = thrust_n / 1000.0
            isp = isp_stream()
            stage_dv = stage_dv_stream()
            total_dv = sum(stage.delta_v for stage in vessel.stages)
            apoapsis = apoapsis_stream()
            periapsis = periapsis_stream()

            radius = body.equatorial_radius + altitude
            local_g = body.gravitational_parameter / (radius ** 2)
            weight_n = (total_mass * 1000.0) * local_g
            twr = (thrust_n / weight_n) if weight_n > 0 else 0.0

            # --- Track flight-wide stats for the summary row ---
            if initial_total_dv is None:
                initial_total_dv = total_dv
            peak_dynamic_pressure = max(peak_dynamic_pressure, dyn_q)
            peak_twr = max(peak_twr, twr)

            if (
                lko_summary is None
                and apoapsis >= LKO_ALTITUDE_THRESHOLD_M
                and periapsis >= LKO_ALTITUDE_THRESHOLD_M
            ):
                lko_summary = {
                    "config_name": config_name,
                    "time_to_lko_s": round(mission_time, 2),
                    "initial_total_dv_ms": round(initial_total_dv, 2),
                    "dv_remaining_at_lko_ms": round(total_dv, 2),
                    "dv_spent_to_lko_ms": round(initial_total_dv - total_dv, 2),
                    "current_stage_dv_at_lko_ms": round(stage_dv, 2),
                    "peak_dynamic_pressure_pa": round(peak_dynamic_pressure, 2),
                    "peak_twr": round(peak_twr, 3),
                    "apoapsis_m": round(apoapsis, 1),
                    "periapsis_m": round(periapsis, 1),
                }
                print(
                    f"\n>>> LKO reached at T+{mission_time:.1f}s -- "
                    f"{total_dv:.0f} m/s delta-v remaining for the rest of the mission!\n"
                )

            writer.writerow([
                round(mission_time, 2),
                round(altitude, 2),
                round(surf_speed, 2),
                round(orb_speed, 2),
                round(v_speed, 2),
                round(h_speed, 2),
                round(pitch, 2),
                round(dyn_q, 2),
                round(total_mass * 1000.0, 2),  # converted to kg
                round(thrust_kn, 2),
                round(twr, 3),
                round(isp, 2),
                round(stage_dv, 2),
                round(total_dv, 2),
                round(apoapsis, 2),
                round(periapsis, 2),
            ])

            time.sleep(SLEEP_INTERVAL)

    except KeyboardInterrupt:
        print("\nLogging stopped by user.")
    finally:
        print(f"Data successfully saved to {LOG_FILENAME}.")

        if lko_summary is not None:
            file_exists = os.path.exists(COMPARISON_FILENAME)
            with open(COMPARISON_FILENAME, mode="a", newline="") as comp_file:
                comp_writer = csv.DictWriter(comp_file, fieldnames=list(lko_summary.keys()))
                if not file_exists:
                    comp_writer.writeheader()
                comp_writer.writerow(lko_summary)
            print(f"Added summary for '{config_name}' to {COMPARISON_FILENAME}.")
        else:
            print(
                f"LKO was not reached during this recording (apoapsis/periapsis never "
                f"both exceeded {LKO_ALTITUDE_THRESHOLD_M}m), so no comparison row was added."
            )