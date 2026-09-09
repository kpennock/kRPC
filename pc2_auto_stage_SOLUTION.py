"""
Programming Track -- Challenge 2: Auto-Stage  (SOLUTION)
=============================================================
Phase 01 tie-in: staging -- "drop it the instant it's empty."

New ideas: while loops, if/else conditionals, the resources API,
reacting to a number crossing a threshold. This threshold-watching
pattern is the one every later script in this track reuses.

Run this AFTER you've already launched -- it manages staging only, it
doesn't launch or throttle up for you.
"""

import krpc
import time

conn = krpc.connect(name="PC2 - Auto Stage")
vessel = conn.space_center.active_vessel

# --- Configure this for your own rocket ----------------------------------
# Check the in-game staging list before running: which stage number
# holds your CURRENTLY BURNING engine's fuel, and is it LiquidFuel or
# SolidFuel?
STAGE_TO_WATCH = vessel.control.current_stage - 1
RESOURCE_NAME = "LiquidFuel"      # or "SolidFuel"
EMPTY_THRESHOLD = 0.5             # units remaining before we call it "empty"
# ---------------------------------------------------------------------------

print(f"Watching stage {STAGE_TO_WATCH} for {RESOURCE_NAME}...")

while STAGE_TO_WATCH >= 0:
    resources = vessel.resources_in_decouple_stage(stage=STAGE_TO_WATCH, cumulative=False)
    amount = resources.amount(RESOURCE_NAME)
    print(f"  stage {STAGE_TO_WATCH} {RESOURCE_NAME}: {amount:,.1f} units")

    if amount < EMPTY_THRESHOLD:
        print(f"  -> stage {STAGE_TO_WATCH} empty, staging!")
        vessel.control.activate_next_stage()
        STAGE_TO_WATCH -= 1
        time.sleep(1)
    else:
        time.sleep(0.5)

print("Done -- reached stage 0, nothing left to watch.")
