select cast(valuation_date as date) as valuation_date,
       cast(instrument_id as varchar) as instrument_id,
       cast(unit_price as decimal(18, 6)) as unit_price
from {{ ref('prices') }}
