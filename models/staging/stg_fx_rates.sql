select cast(valuation_date as date) as valuation_date,
       cast(currency as varchar) as currency,
       cast(rate_to_eur as decimal(18, 8)) as rate_to_eur
from {{ ref('fx_rates') }}
