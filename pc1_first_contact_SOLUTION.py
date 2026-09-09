"""
Programming Track -- Challenge 1: First Contact  (SOLUTION)
==============================================================
Phase 00 tie-in: forces, mass, and thrust.

New ideas: connecting to kRPC, reading one-off live values, writing
your first function, formatted printing.
"""

import krpc

conn = krpc.connect(name="PC1 - First Contact")
vessel = conn.space_center.active_vessel


def compute_twr(thrust, mass, g):
    """Thrust-to-weight ratio: TWR = F_thrust / (m * g)."""
    weight = mass * g
    return thrust / weight


# Live numbers, straight from the game -- no hand-copying off KER.
thrust = vessel.available_thrust          # newtons
mass = vessel.mass                        # kg
g = vessel.orbit.body.surface_gravity     # m/s^2, this body's surface gravity

twr = compute_twr(thrust, mass, g)

print(f"Vessel:  {vessel.name}")
print(f"Thrust:  {thrust:,.0f} N")
print(f"Mass:    {mass:,.1f} kg")
print(f"g:       {g:.3f} m/s^2")
print(f"TWR:     {twr:.2f}   <- compute_twr(thrust, mass, g)")
print(f"\nCompare this to KER's TWR readout -- they should match closely.")
print(f"(If they don't: check whether KER is reading wet mass, or a")
print(f" different g, and see if that explains the gap.)")
