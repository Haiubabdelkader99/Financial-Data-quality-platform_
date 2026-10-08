# Engineering decisions

1. **DuckDB instead of Snowflake for v1:** reproducible local execution without paid accounts or secrets.
   SQL modeling and tests are demonstrated; Snowflake operation/performance is not.
2. **dbt seed fixtures:** transparent, reviewable source snapshots. A live connector would replace ingestion.
3. **Fixed-point decimals:** financial arithmetic avoids binary floating-point storage of monetary values.
4. **Left joins for enrichment:** preserve unknown/missing references so tests detect them instead of losing holdings.
5. **Full outer reconciliation:** missing internal or custodian records are explicit statuses.
6. **Views for staging/intermediate, tables for marts:** limited duplicated storage and convenient downstream exports.
7. **Full rebuild:** predictable small-fixture behaviour. Incremental strategy requires scale, late-data and rerun requirements.
8. **No unmeasured speed claims:** performance optimization needs realistic data volumes, EXPLAIN and measured baselines.

## Snowflake roadmap (not implemented or tested)
- Replace dbt-duckdb with dbt-snowflake and use environment-based authentication; never commit secrets.
- Review numeric precision, SQL compatibility, database/schema configuration and seed loading.
- Replace fixed seed inputs with source contracts and a real freshness expectation.
- Run the same integrity tests and golden fixture checks on Snowflake before claiming portability.
- Benchmark representative workloads with query history/profile and warehouse credits.
- Consider incremental models only after defining late-arriving corrections and unique-key contracts.
- Define warehouse auto-suspend, least-privilege access and cost monitoring.

## Suggested next contribution
Create a branch `feature/reconciliation-relative-tolerance` and propose a documented tolerance policy:
break only when absolute AND relative differences exceed business-approved limits.
Add edge-case fixtures around both boundaries; update the runbook and open a PR.
This is an exercise, not an instruction to weaken existing controls.
