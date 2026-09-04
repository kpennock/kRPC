"""
Phase 01/02 kRPC Intro -- Script 2: Auto-staging
==================================================
Goal: write the first real piece of automation -- a script that watches
a stage's fuel and stages the instant it runs dry, instead of you
clicking (or pressing space) at the right moment by eye.

This is the manual's "drop it the instant it's empty" idea from the
rocket-equation section, written as code. Watching a number and reacting
the moment it crosses a threshold -- that's the single most common
pattern in every autopilot script you'll write from here on, including
the hover controller later in this series.

Run this AFTER you've already launched and are underway -- it manages
staging only, it doesn't launch the rocket or throttle it up for you.
Combine it with your own launch sequence (or Script 3) for a fuller
automated ascent.
"""

import krpc
import time

conn = krpc.connect(name="02 - Auto Stage")
vessel = conn.space_center.active_vessel

# --- Configure this for your own rocket ----------------------------------
# Open the staging list in KSP before running this and check:
#   - which stage number holds the fuel for your CURRENTLY BURNING engine
#   - whether that stage burns LiquidFuel or SolidFuel
# kRPC numbers "decouple stages" the same way the in-game staging list
# does. vessel.control.current_stage tells you where the game thinks you
# are right now -- print it in the KSP debug console (Alt+F2) if you're
# not sure which number to start with.
STAGE_TO_WATCH = vessel.control.current_stage - 1
RESOURCE_NAME = "LiquidFuel"      # or "SolidFuel"
EMPTY_THRESHOLD = 0.5             # units remaining before we call it "empty"
# ---------------------------------------------------------------------------

print(f"Watching stage {STAGE_TO_WATCH} for {RESOURCE_NAME}...")

while STAGE_TO_WATCH >= 0:
    # resources_in_decouple_stage scopes the resource query to just the
    # parts that decouple at this stage number, not the whole rocket --
    # otherwise fuel sitting in a stage you haven't reached yet would
    # make it look like you're never running low.
    resources = vessel.resources_in_decouple_stage(stage=STAGE_TO_WATCH, cumulative=False)
    amount = resources.amount(RESOURCE_NAME)
    print(f"  stage {STAGE_TO_WATCH} {RESOURCE_NAME}: {amount:,.1f} units")

    if amount < EMPTY_THRESHOLD:
        print(f"  -> stage {STAGE_TO_WATCH} empty, staging!")
        vessel.control.activate_next_stage()
        STAGE_TO_WATCH -= 1
        time.sleep(1)  # give the new stage a moment to register before we
                        # start reading its resources
    else:
        time.sleep(0.5)

print("Done -- reached stage 0, nothing left to watch.")
