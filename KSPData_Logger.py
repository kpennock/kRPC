import csv
import time
import krpc

# Connect to KSP
conn = krpc.connect(name='Telemetry Logger')
vessel = conn.space_center.active_vessel

# Set up data streams
flight = vessel.flight()
orbit = vessel.orbit

# Open CSV file for writing
with open('flight_telemetry.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Write header
    writer.writerow([
        'time_s', 
        'altitude_m', 
        'surface_velocity_ms', 
        'orbital_velocity_ms', 
        'stage_deltav_vac_ms', 
        'total_deltav_vac_ms',
        'dynamic_pressure_pa'
    ])
    
    print("Logging telemetry... Press Ctrl+C to stop.")
    try:
        while True:
            t = conn.space_center.ut
            alt = flight.mean_altitude
            surf_spd = flight.speed
            orb_spd = orbit.speed
            dyn_q = flight.dynamic_pressure
            
            # Delta-v via vessel stage stats
            stage_dv = vessel.stage_stats.current_stage_delta_v
            total_dv = vessel.stage_stats.total_delta_v
            
            writer.writerow([t, alt, surf_spd, orb_spd, stage_dv, total_dv, dyn_q])
            time.sleep(0.2)  # Log at 5 Hz
    except KeyboardInterrupt:
        print("\nLogging complete. File saved to flight_telemetry.csv")