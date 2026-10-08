# Local validation evidence

Validated on 7 October 2026 with Python 3.12, dbt Core 1.12.5, dbt-duckdb 1.9.6 and DuckDB 1.4.1 on Linux.
Primary dependencies and resolved dependency constraints are included for reproducibility.
Windows commands are supplied, but no Windows execution is claimed.

- `python scripts/run_pipeline.py`: completed, 6 seeds, 7 models and 30 data tests; no failed or skipped nodes.
- `python scripts/verify_demo.py`: all six independently specified portfolio totals matched;
  18 positions, 1 reconciliation exception (EUR -50), 4 concentration breaches.
- `python scripts/failure_drill.py`: duplicate holding, missing USD FX and unknown instrument each failed
  the intended data test and returned a failed build in an isolated temporary copy.
- Documentation catalog and model manifest generated successfully.
- HTML, CSV and local JSON alert exports generated successfully.
- Build test evidence is preserved in target/build_run_results.json before documentation generation.

The examples directory contains synthetic output from that run. This is not a performance benchmark,
production deployment, Windows compatibility certification or a completed GitHub Actions run.

To reproduce: install requirements.txt in a Python 3.12 virtual environment and execute the three commands above.
