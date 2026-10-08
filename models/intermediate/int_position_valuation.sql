-- Long-only instruments. Bond prices are simplified unit prices, not clean % quotes.
select p.position_id, p.valuation_date, p.portfolio_id, p.instrument_id,
       i.instrument_name, i.asset_class, i.currency, p.quantity,
       px.unit_price, fx.rate_to_eur,
       cast(p.quantity * px.unit_price * fx.rate_to_eur as decimal(20, 6))
           as market_value_eur
from {{ ref('stg_positions') }} p
left join {{ ref('instruments') }} i on p.instrument_id = i.instrument_id
left join {{ ref('stg_prices') }} px
    on p.instrument_id = px.instrument_id and p.valuation_date = px.valuation_date
left join {{ ref('stg_fx_rates') }} fx
    on i.currency = fx.currency and p.valuation_date = fx.valuation_date
