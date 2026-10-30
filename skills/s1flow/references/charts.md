# Render a comparison report

Use this when a human wants a report or figures for an article. An agent can read the same multiple-metric
snapshot as compact text or JSON without rendering it.

```bash
s1flow report <task> --out report
python <skill>/scripts/charts.py report/comparison.json --out comparison.html
```

The renderer is standard-library Python. It reads a saved v2 snapshot, without evaluation imports, model calls,
rescoring, task reads, adoption or activation. The first command needs `s1flow[eval]`; rendering does not.
Regenerate older v1 snapshots rather than treating their absent metrics as measured.

The report begins with the Task objective against API cost. Either axis can switch to another recorded metric
or p90 latency. Add a second relationship only when useful; recorded 95% intervals and focused axis ranges
are optional. Coverage objectives also show observed accepted accuracy in the default table. This changes
the view, not scores or reading rules. Number tags identify candidates without shifting measured coordinates.
The candidate-by-metric table below keeps every candidate in model/variant order; choose its visible columns.
Candidates missing either axis measurement are named below the plot and remain in the table.
No recommendation, overall score, eligibility filter, adoption form or command builder is included.
Below-target results remain visible. Reference conditions do not represent the person's entire decision criteria.

Every figure includes its metric definition, development population, source and snapshot identity. SVG and PNG
buttons save standalone figures for reports or articles. The HTML also has a print layout. Preserve captions and
conditions when using an exported figure; synthetic previews are not evidence about real models.

Plain-answer metrics, configured objective scores, and coverage/accepted-accuracy pairs have different readings.
Their definitions remain beside the figures and in Evaluation context. Show the answered count and refusal/failure
counts when comparing populations. Unknowns stay unknown; costs retain billed/estimated/mixed provenance, and speed
measurements with different or missing concurrency/retry conditions are explicitly qualified.

Probability diagnostics are optional. Select a candidate to inspect the stored acceptance curve, binary
precision/recall curve or calibration where applicable. They are exploratory dev values, not the cross-validated
comparison scores or a policy editor. Choice uses genuine selected-answer probabilities; Box uses recorded box
confidence and IoU. Missing probability signals produce an unavailable reason, not invented curves. Score remains
unsupported for evaluation comparison.

Only labelled development cases are exposed. Final held-out test results are read by explicit adoption or final
check commands, not by this report. A human owns the criteria and choice; an agent selects only when authorized
with those criteria. The shared snapshot supplies the facts to both.
