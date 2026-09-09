"""
Phase 01/02 kRPC Intro -- Script 1: Hello, kRPC
=================================================
Goal: connect to a running KSP game and read live telemetry -- the same
numbers KER shows you, but from your own code instead of an add-on panel.

Before running:
  1. Launch KSP, load a save, and have a rocket on the pad or already
     flying.
  2. Make sure the kRPC mod is installed and its in-game server is
     started (the kRPC toolbar icon in KSP -> Start server / Start
     Server on Client Connect).
  3. pip install krpc
  4. Run this file from a normal terminal: python 01_hello_krpc.py
"""

import krpc
import time

# krpc.connect() opens a connection to the kRPC server running inside
# KSP. name=... is just a label -- it shows up in the in-game kRPC
# window so you can tell which script is currently connected.
conn = krpc.connect(name="01 - Hello Commander Connor Pennock.  We are honored to serve you!")

# space_center is kRPC's window into the whole game: vessels, celestial
# bodies, universal time, all of it. active_vessel is whichever ship
# you're currently controlling in KSP.
vessel = conn.space_center.active_vessel

print(f"Connected to vessel: {vessel.name}")
print(f"Currently at:        {vessel.orbit.body.name}")

# vessel.flight(reference_frame) gives you altitude/speed/etc measured
# relative to whatever frame you hand it. The body's own reference_frame
# means "relative to the ground" -- altitude and speed the same way the
# navball shows them. We'll use a different frame for orbital quantities
# in Script 3, once "speed relative to the ground" isn't the number we
# actually want.
flight = vessel.flight(vessel.orbit.body.reference_frame)

# One-off reads: ask kRPC for a single current value.
print(f"\nOne-off readings:")
print(f"  altitude:      {flight.mean_altitude:>12,.1f} m")
print(f"  surface speed: {flight.speed:>12,.1f} m/s")
print(f"  apoapsis alt:  {vessel.orbit.apoapsis_altitude:>12,.1f} m")
print(f"  periapsis alt: {vessel.orbit.periapsis_altitude:>12,.1f} m")

# ---------------------------------------------------------------------
# STREAMS
# ---------------------------------------------------------------------
# Reading a value once is fine for a snapshot, but a script that has to
# *watch* a number over time -- which is most of what an autopilot does
# -- should use a stream instead of calling the getter over and over.
# A stream tells the kRPC server "keep this value updated for me
# automatically," which is far more efficient over a long-running
# script, and it's the pattern every later script in this series
# builds on.
# ---------------------------------------------------------------------
altitude_stream = conn.add_stream(getattr, flight, "mean_altitude")
speed_stream = conn.add_stream(getattr, flight, "speed")

print("\nStreaming telemetry for 10 seconds (Ctrl+C to stop early)...")
try:
    for _ in range(10):
        print(f"  alt={altitude_stream():>10,.1f} m   speed={speed_stream():>8,.1f} m/s")
        time.sleep(1)
finally:
    # Always close streams you're done with -- they keep sending updates
    # from the game until you do, which wastes bandwidth on a long
    # session and can pile up if a script creates new ones in a loop.
    altitude_stream.remove()
    speed_stream.remove()
    print("Streams closed.")
