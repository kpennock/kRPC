# Programming Track: Learn kRPC by Building an Autopilot

A second track that runs alongside the main mission notebook, aimed
squarely at durable skill rather than this project's grade: six short
challenges, each teaching one new Python/kRPC idea on top of the last,
ending with a script that actually hovers or lands a craft on its own.
The goal isn't just "make it to Duna" — it's that a few months from
now, on whatever the next KSP project turns out to be, this group
already knows how to connect to a running game, read its state, and
make it do something back.

This track is deliberately separate from `mission_analysis.py`. That
toolkit *analyzes* flights after they've landed; this track *flies*
them, live, while they're in the air. Both are "programming," but
they're different skills — this is the control-and-automation half.

**How to run it:** each challenge is optional and roughly 20–30
minutes, sized to slot in next to (not instead of) that phase's design
challenge — a "while we wait for the next launch window" activity, or
a rotating role where one teammate drives the code each week. Every
challenge ships as a `_STARTER.py` file (the setup is done, the new
idea is left as TODOs) and a `_SOLUTION.py` file (instructor reference
— don't hand this out up front). Nothing here is required to complete
the main manual; treat it as a fifth thing groups can pick up if
they've got room in the schedule.

## The progression

| # | Pairs with | New idea | What it builds |
|---|---|---|---|
| 1 · First Contact | Phase 00 | Connecting to kRPC, one-off reads, your first function | Reads live thrust/mass/g and computes TWR by hand-in-code |
| 2 · Auto-Stage | Phase 01 | `while` loops, `if`/`else`, reacting to a threshold | Stages automatically the instant a stage's fuel runs dry |
| 3 · Auto-Circularize | Phase 02 | A function around a real equation, autopilot orientation | Codes `v = sqrt(μ/r)` and uses it to end a circularization burn |
| 4 · Vis-Viva Checker | Phase 03 | A 3-parameter function, a continuous predict-vs-measure loop | Verifies energy conservation live, the whole way around an ellipse |
| 5 · Descent Watchdog | Phase 05 | Watching several values at once, a running list | Flags g-force and speed/altitude danger live, reports the worst reading |
| **Capstone · Hover or Land** | Phase 06 | Proportional control, a multi-phase state machine | Hovers indefinitely, or free-falls / brakes / eases down to landing |

Each challenge's new idea is additive — the capstone uses all six.

## Challenge 1 — First Contact

*Files: `pc1_first_contact_STARTER.py` / `_SOLUTION.py`*

**Goal:** connect to kRPC, read your own rocket's numbers, and write
your first function — one that turns those numbers into TWR, the same
way you already do by hand.

**Before you start:** have KSP running with a rocket on the pad and
the kRPC server started (see the setup note at the bottom of this
doc).

**Checkpoint:** does your script's TWR match KER's live readout? If
not, that's a genuinely useful bug to chase — usually a wet-vs-dry
mass mismatch or a different `g`.

## Challenge 2 — Auto-Stage

*Files: `pc2_auto_stage_STARTER.py` / `_SOLUTION.py`*

**Goal:** automate the exact idea from Phase 01's staging section —
drop a stage the instant it's empty — instead of clicking or pressing
space at the right moment by eye.

**Before you start:** launch and get underway first; this script
manages staging only. Check your craft's staging list in-game so you
know which stage number and which fuel type (`LiquidFuel` vs.
`SolidFuel`) to watch.

**Reflection:** what happens if `EMPTY_THRESHOLD` is set too low? Too
high? Try both and see the failure mode for each.

## Challenge 3 — Auto-Circularize

*Files: `pc3_auto_circularize_STARTER.py` / `_SOLUTION.py`*

**Goal:** the first script that really *flies* — it points itself
prograde and cuts the engine using a live-computed number, not a
timer. This is Phase 02's equation, typed in as a function, deciding
when the burn is done.

**Before you start:** have an ascending trajectory with an apoapsis
already set above the atmosphere (~70+ km at Kerbin).

**Checkpoint:** how close did `v_circular` land to what KER reports
once the burn finishes? A perfect match isn't the point — explaining
any gap is.

## Challenge 4 — Vis-Viva Live-Checker

*Files: `pc4_vis_viva_checker_STARTER.py` / `_SOLUTION.py`*

**Goal:** a script that doesn't fly anything — it watches. While
coasting on an unpowered ellipse, it predicts your speed from vis-viva
and compares it to the measured speed, continuously, the whole way
around the orbit.

**Before you start:** get onto an elliptical coast first (Design
challenge 4's apoapsis-raising burns work well) and make sure the
engine is off — vis-viva only holds when nothing's thrusting.

**Reflection:** the predicted-vs-measured gap should stay small and
roughly constant everywhere on the orbit, both near periapsis and near
apoapsis. What would it mean if the gap grew steadily larger over
time instead?

## Challenge 5 — Descent Watchdog

*Files: `pc5_descent_watchdog_STARTER.py` / `_SOLUTION.py`*

**Goal:** a monitoring script — watch several numbers at once, and
raise a flag the instant one crosses a safety limit you set yourself.
This is the crew-safety g-limit idea from Phase 07, built early and
tried out during Phase 05's aerobraking passes instead.

**Before you start:** run it live during an aerobraking pass or a
reentry so there's actually a g-force to watch.

**Checkpoint:** after a pass, what was the max g-force logged? Compare
it across a shallow vs. a deep pass (Design challenge 6) — the
watchdog turns that comparison into a live readout instead of
something you'd only see afterward in a CSV.

## Capstone — Hover or Land

*Files: `capstone_hover_or_land_STARTER.py` / `_SOLUTION.py`*

**Goal:** the payoff. Every challenge above built one ingredient —
this combines all of them into a script that either hovers
indefinitely or executes a real suicide burn to a soft touchdown.

Two modes, `HOVER` and `LAND`, sharing one proportional-control
function: hovering is just landing with a target speed of zero
instead of a touchdown. **Get `HOVER` fully working on Kerbin before
attempting `LAND`** — same reasoning as the manual's "test on Kerbin
before you commit to Duna" habit elsewhere.

**Before you start:** an unmanned test craft, SAS-capable, over open
level ground, with more fuel margin than you think you need.

**Reflection:** the `gain` values in `throttle_for_target_speed()` are
tuned by hand, by guessing and re-flying — not derived from an
equation. Try a much larger gain and watch what happens (hint: it
should feel familiar from the manual's proportional-control note about
oscillation). That tuning-by-feel process is itself worth naming: it's
exactly how real engineers tune control systems before more advanced
methods take over.

**Where this could go next time:** a full PID controller (adding
"how long has the error persisted" and "how fast is the error
changing" on top of today's plain proportional term), horizontal
translation to a chosen landing site instead of straight down, or
scripting the transfer-burn maneuver node itself using vector math —
all reasonable next steps for whatever Project 2 turns out to be.

---

### Setup (once, for the whole track)

1. Install the kRPC mod into KSP's `GameData` folder.
2. `pip install krpc`
3. In-game: click the kRPC toolbar icon and start the server before
   running any script.
4. Run scripts from a normal terminal: `python pc1_first_contact_STARTER.py`
