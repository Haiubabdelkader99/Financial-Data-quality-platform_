# Architecture and data contracts

## Grains and contracts

| Dataset | Grain | Critical invariant |
|---|---|---|
| portfolios | portfolio_id | EUR base currency; threshold in (0,1] |
| instruments | instrument_id | Known currency and unique identifier |
| positions / stg_positions | position_id; also date/portfolio/instrument | One long-only holding per business key |
| prices / stg_prices | date/instrument | Positive unit price |
| fx_rates / stg_fx_rates | date/currency | Positive EUR-per-unit rate; EUR=1 |
| custodian_totals | date/portfolio | Independent reported holdings value |
| int_position_valuation | position_id | Every input survives once; non-null value |
| fct_portfolio_daily | date/portfolio | Total equals rounded sum of holdings |
| fct_reconciliation | date/portfolio | Full coverage of internal and reference keys |
| fct_concentration | date/portfolio/instrument | Weights sum to 1 within rounding tolerance |

EUR value = quantity × unit price × EUR-per-currency-unit FX.
For P001 on 2026-09-28: 100×100 + 50×150×0.90 + 100×98 = EUR 26,550.
Values are not rounded per position before aggregation; reporting totals are rounded to cents.

## Lineage

- `positions` → `stg_positions` → `int_position_valuation`.
- `instruments`, `prices` → `stg_prices`, `fx_rates` → `stg_fx_rates` enrich valuation.
- Valuation + `portfolios` → daily totals.
- Daily totals + `custodian_totals` → reconciliation.
- Valuation + daily totals + portfolio thresholds → concentration.
- Tested marts → Python exports, report and local alert summary.

`dbt docs generate` writes manifest/catalog artifacts; `dbt docs serve --profiles-dir .` displays the DAG.
This is dbt model lineage, not a claim of automated end-to-end column lineage.

## Structural failures versus business exceptions

A duplicate price or missing FX is a structural defect: block the affected build and report publication.
A correctly identified custodian break or risk breach is a business exception: publish the exception for
review without pretending that pipeline execution failed. This distinction is intentional.

## Operational boundary

CSV seeds simulate source-system extracts. There is no live ingestion scheduler, cloud deployment,
email notification, multi-user service or regulatory sign-off. These are future integration boundaries.
