# kRPC programming intro — Phase 01/02 companion scripts

Four scripts, meant to be stepped through in order, that introduce kRPC
programming alongside Phase 01 (the rocket equation & staging) and
Phase 02 (circular orbits & Kepler's third law). This is a separate
track from `mission_analysis.py` — that toolkit analyzes flights after
the fact; these scripts *fly the rocket*, live, while it's in the air.
Same Python, very different skill: control and automation instead of
data analysis.

## Setup (once)

1. Install the kRPC mod into your KSP GameData folder.
2. `pip install krpc`
3. In-game: click the kRPC toolbar icon and start the server before
   running any script below.

## The sequence

| Script | Introduces | Ties to |
|---|---|---|
| `01_hello_krpc.py` | Connecting, the vessel object, reference frames, one-off reads vs. streams | Phase 00/01 — reading live telemetry instead of relying on KER's panel |
| `02_auto_stage.py` | Watching a resource, reacting past a threshold, `vessel.control` | Phase 01 — automates the manual's own "drop it the instant it's empty" idea |
| `03_auto_circularize.py` | The autopilot object, prograde orientation, coding an equation from the manual straight into a control script | Phase 02 — literally executes `v = sqrt(μ/r)` to decide when to cut the engine |
| `04_hover_preview_BONUS.py` | Proportional (P) control — react to error, react to rate of change | Preview of Phase 06's Duna hover/landing goal, flown safely at Kerbin first |

Have each group run Script 1 as-is first, just to see live numbers move.
Before Script 2, ask them to predict out loud what will happen if
`STAGE_TO_WATCH` is set one number too high or too low — a good way to
surface whether they actually understand what "decouple stage" means
before the code does it for them. Script 3 is the payoff moment: the
exact equation from the Phase 02 equation box, typed in as
`math.sqrt(mu / r)`, actually flying the ship. Script 4 is explicitly
optional — flag it as "a look ahead," not something to grade.

## Where this goes next

Script 4 stops well short of an actual landing: it holds a fixed
altitude over flat, known ground on Kerbin, with gravity as the only
real complication. A real Duna hover-to-landing autopilot for Phase 06
needs more: descent-rate control instead of just altitude-hold, a
target of *zero* rather than a fixed hover height, Duna's much weaker
gravity changing every gain constant, and eventually a full suicide
burn that switches from "descend fast to save fuel" to "decelerate
hard" at the right moment — using the same `h = v₀² / (2·(a_thrust − g))`
equation already in the Phase 06 worked example.

Rather than build all of that speculatively, this drop stops at the
preview — let me know how the walkthrough goes with students and which
direction you want to take it (a guided descent-rate controller next,
straight to a full suicide-burn autopilot, something in between), and
I'll build the next stage of scripts to match.
