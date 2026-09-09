import csv
import math
import time
import krpc

# Target output file & logging configuration
LOG_FILENAME = "flight_telemetry.csv"
SAMPLE_RATE_HZ = 5.0  # 5 samples per second (0.2s interval)
SLEEP_INTERVAL = 1.0 / SAMPLE_RATE_HZ

print("Connecting to Kerbal Space Program via kRPC...")

try:
    print("Attempting to connect to kRPC...")
    conn = krpc.connect(
        name='Data Logger',
        address='127.0.0.1',  # If this fails, try '0.0.0.0' or 'localhost'
        rpc_port=50000,
        stream_port=50001
    )
    print("Successfully connected to KSP!")
    vessel = conn.space_center.active_vessel
    print(f"Connected to vessel: {vessel.name}")
except Exception as e:
    print(f"Connection failed: {e}")
    exit(1)

vessel = conn.space_center.active_vessel
body = vessel.orbit.body

# Flight frame references
flight_surface = vessel.flight(vessel.surface_reference_frame)
flight_orbital = vessel.flight(vessel.orbital_reference_frame)

# Note: vessel.delta_v is a plain float (current stage's delta-v, given
# current atmospheric conditions) -- not an object with sub-properties.
# There's no single "total delta-v across all remaining stages" RPC, so
# that value is computed each loop iteration by summing vessel.stages.

print(f"Connected to vessel: {vessel.name}")
print("Setting up telemetry data streams...")

# Establish low-latency streams
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
stage_dv_stream = conn.add_stream(getattr, vessel, "delta_v")
apoapsis_stream = conn.add_stream(getattr, vessel.orbit, "apoapsis_altitude")
periapsis_stream = conn.add_stream(getattr, vessel.orbit, "periapsis_altitude")

# CSV File Headers
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

# Baseline initial values for delta-calculations
start_ut = ut_stream()

print(f"Starting flight recording to '{LOG_FILENAME}' at {SAMPLE_RATE_HZ} Hz.")
print("Press Ctrl+C at any point to stop logging.")

with open(LOG_FILENAME, mode="w", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(headers)

    try:
        while True:
            current_ut = ut_stream()
            mission_time = current_ut - start_ut

            # Fetch stream values
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
            # Sum delta-v across all remaining stages (not stream-able as
            # a single RPC value, so recomputed each iteration)
            total_dv = sum(stage.delta_v for stage in vessel.stages)
            apoapsis = apoapsis_stream()
            periapsis = periapsis_stream()

            # Calculate local gravity & current TWR
            # g = G * M / r^2
            radius = body.equatorial_radius + altitude
            local_g = body.gravitational_parameter / (radius ** 2)

            # Weight = mass (kg) * g
            weight_n = (total_mass * 1000.0) * local_g
            twr = (thrust_n / weight_n) if weight_n > 0 else 0.0

            # Write row
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