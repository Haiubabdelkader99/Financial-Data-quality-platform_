select 'prices' as dataset from {{ ref('stg_prices') }}
where unit_price <= 0 or unit_price is null or valuation_date is null or instrument_id is null
union all
select 'fx' from {{ ref('stg_fx_rates') }}
where rate_to_eur <= 0 or rate_to_eur is null or valuation_date is null or currency is null
   or (currency = 'EUR' and rate_to_eur <> 1)
union all
select 'positions' from {{ ref('stg_positions') }} where quantity < 0
union all
select 'portfolios' from {{ ref('portfolios') }}
where concentration_limit <= 0 or concentration_limit > 1 or concentration_limit is null
union all
select 'custodian' from {{ ref('custodian_totals') }}
where portfolio_id is null or valuation_date is null or reported_value_eur is null
