"""
Programming Track -- Challenge 1: First Contact  (STARTER)
==============================================================
Phase 00 tie-in: forces, mass, and thrust.

New ideas: connecting to kRPC, reading one-off live values, writing
your first function, formatted printing.

Fill in the TODOs below. Nothing here flies the rocket -- it's fine
to run this sitting on the pad.
"""

import krpc

conn = krpc.connect(name="PC1 - First Contact")
vessel = conn.space_center.active_vessel


def compute_twr(thrust, mass, g):
    """
    TODO: return TWR = F_thrust / (m * g)
    (This is Phase 00's equation, exactly as written in the manual --
    just turn it into working code.)
    """
    pass  # <-- replace this with your calculation


# TODO: pull these three values live from kRPC instead of leaving them
# as None. Hints:
#   thrust -> vessel.available_thrust
#   mass   -> vessel.mass
#   g      -> vessel.orbit.body.surface_gravity
thrust = None
mass = None
g = None

twr = compute_twr(thrust, mass, g)

print(f"Vessel:  {vessel.name}")
print(f"Thrust:  {thrust}")
print(f"Mass:    {mass}")
print(f"g:       {g}")
print(f"TWR:     {twr}")
print("\nCompare this number to KER's live TWR readout on the pad.")
