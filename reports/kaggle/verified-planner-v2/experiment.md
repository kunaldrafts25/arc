# Full public comparison after functional/adoption pilot

Control: `kunalsinghh25/arc-hydra-duck-m2-baseline/3`.
Candidate: `kunalsinghh25/arc-hydra-verified-planner/2`.

Both arms: all 25 public games, one pass, the original Intel AutoRound target
and draft, original v2.5.3 serving stack, original scheduler, and 7,200 seconds
after confirmed model readiness. Both use full public diagnostics; the candidate
also retains its lightweight lifecycle/mechanical event evidence. Notebook
timeouts are 12,000 seconds. No official submission and no weight training.

Control source is byte-identical to the completed baseline/2 upload. Candidate
helper/installer hashes are unchanged from the completed five-game GPU pilot
and passed CPU gate. It changes action enforcement, system guidance and lifecycle
instrumentation, so this compares complete agent configurations rather than
isolating one mechanism. Sampling is stochastic and seeds are not paired.

Collect final analysis, per-game scores/levels, completion curves, model tokens,
mechanical helper adoption, replay failures and prospective mismatches. Confirm
all games have substantive model gameplay. The older five-game pilot control's
timer included startup and cannot establish a quality gain for this candidate.

Promotion requires the complete evidence, not early snapshots or a successful
upload. A single public comparison does not prove hidden score improvement or
completion of the official >71.48 objective.
