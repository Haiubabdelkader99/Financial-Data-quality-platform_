-- Grain: one portfolio per valuation date. Rounding happens after aggregation.
select v.valuation_date, v.portfolio_id, p.portfolio_name,
       count(*) as position_count,
       cast(round(sum(v.market_value_eur), 2) as decimal(20, 2)) as total_value_eur
from {{ ref('int_position_valuation') }} v
left join {{ ref('portfolios') }} p on v.portfolio_id = p.portfolio_id
group by v.valuation_date, v.portfolio_id, p.portfolio_name
