select
    cast(position_id as varchar) as position_id,
    cast(valuation_date as date) as valuation_date,
    cast(portfolio_id as varchar) as portfolio_id,
    cast(instrument_id as varchar) as instrument_id,
    cast(quantity as decimal(18, 6)) as quantity
from {{ ref('positions') }}
