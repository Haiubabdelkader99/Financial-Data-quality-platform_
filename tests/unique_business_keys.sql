-- Duplicate reference keys would multiply values in joins.
select 'prices' as dataset, cast(valuation_date as varchar) as business_date,
       instrument_id as business_key, count(*) as records
from {{ ref('stg_prices') }} group by valuation_date, instrument_id having count(*) > 1
union all
select 'fx_rates', cast(valuation_date as varchar), currency, count(*)
from {{ ref('stg_fx_rates') }} group by valuation_date, currency having count(*) > 1
union all
select 'positions', cast(valuation_date as varchar), portfolio_id || ':' || instrument_id, count(*)
from {{ ref('stg_positions') }}
group by valuation_date, portfolio_id, instrument_id having count(*) > 1
union all
select 'custodian', cast(valuation_date as varchar), portfolio_id, count(*)
from {{ ref('custodian_totals') }} group by valuation_date, portfolio_id having count(*) > 1
