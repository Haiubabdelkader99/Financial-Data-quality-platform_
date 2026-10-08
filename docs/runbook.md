# Operational runbook

## Normal execution
1. Activate the Python environment and run `python scripts/run_pipeline.py`.
2. Confirm exit code 0; inspect `target/run_results.json` and `outputs/alerts.json`.
3. Review reconciliation exceptions and concentration breaches in `outputs/report.html`.
4. For this fixture expect one EUR 50 reconciliation break and four concentration breaches.

## Pipeline failure
- A failure blocks report export. Existing outputs are removed before execution to avoid stale reports.
- Preserve logs and `target/run_results.json`; identify the first failing model/test, not only skipped nodes.
- Inspect upstream seed keys, missing prices/FX and reference relationships.
- Never add `distinct`, zero-fill missing prices or relax a test merely to make execution green.
- Correct the underlying input or transformation in a branch, run all checks, and review the PR.
- Rerun the full build. Confirm affected outputs and downstream totals before accepting results.

## Reconciliation break
1. Confirm portfolio/date/currency alignment and reference completeness.
2. Compare quantities, prices and FX by instrument.
3. Distinguish source-data errors from transformation defects and genuine timing differences.
4. Record owner, investigation, evidence and resolution; never overwrite the reference to match blindly.
5. The known P002 fixture is deliberately EUR 50 higher on the reference side, a simulated valuation break.

## Failure drill
`python scripts/failure_drill.py` injects duplicate holdings, a missing USD FX rate and an unknown instrument
into isolated temporary project copies. It asserts a specific failing test for each case. No manual reset needed.

## Release and rollback
Use feature branches and pull requests. CI must pass; configure GitHub branch protection separately if desired.
For a bad transformation, revert the reviewed commit and rebuild from the unchanged input fixture.
In a real system rollback also requires snapshot/retention policies; this demo does not implement those.

## Escalation design
In production: structural failures → data platform owner; reconciliation → Finance/Risk data owner;
concentration exceptions → Risk owner. Routes, deadlines and paging would be agreed with stakeholders.
This repository writes an alert artifact only and sends no messages.
