-- Instrument weight, not issuer concentration. Demo threshold is not a UCITS rule.
select v.valuation_date, v.portfolio_id, v.instrument_id,
       v.market_value_eur,
       v.market_value_eur / nullif(p.total_value_eur, 0) as weight,
       cast(l.concentration_limit as decimal(8, 6)) as concentration_limit,
       case when v.market_value_eur / nullif(p.total_value_eur, 0)
                      > l.concentration_limit
            then 'BREACH' else 'PASS' end as control_status
from {{ ref('int_position_valuation') }} v
join {{ ref('fct_portfolio_daily') }} p
  on v.portfolio_id = p.portfolio_id and v.valuation_date = p.valuation_date
join {{ ref('portfolios') }} l on v.portfolio_id = l.portfolio_id
