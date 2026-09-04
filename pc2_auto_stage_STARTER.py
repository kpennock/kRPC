"""
Programming Track -- Challenge 2: Auto-Stage  (STARTER)
=============================================================
Phase 01 tie-in: staging -- "drop it the instant it's empty."

New ideas: while loops, if/else conditionals, the resources API,
reacting to a number crossing a threshold.

Fill in the loop body. Run this AFTER you've already launched.
"""

import krpc
import time

conn = krpc.connect(name="PC2 - Auto Stage")
vessel = conn.space_center.active_vessel

STAGE_TO_WATCH = vessel.control.current_stage - 1
RESOURCE_NAME = "LiquidFuel"      # or "SolidFuel" -- check your craft
EMPTY_THRESHOLD = 0.5

print(f"Watching stage {STAGE_TO_WATCH} for {RESOURCE_NAME}...")

while STAGE_TO_WATCH >= 0:
    # TODO 1: get this stage's resources.
    #   hint: vessel.resources_in_decouple_stage(stage=STAGE_TO_WATCH, cumulative=False)
    resources = None

    # TODO 2: read how much RESOURCE_NAME is left in that stage.
    #   hint: resources.amount(RESOURCE_NAME)
    amount = None

    print(f"  stage {STAGE_TO_WATCH} {RESOURCE_NAME}: {amount}")

    # TODO 3: write the if/else.
    #   if amount is below EMPTY_THRESHOLD:
    #     - call vessel.control.activate_next_stage()
    #     - subtract 1 from STAGE_TO_WATCH
    #     - time.sleep(1)  (give the new stage a moment to register)
    #   else:
    #     - time.sleep(0.5) and loop back around to check again

print("Done -- reached stage 0, nothing left to watch.")
