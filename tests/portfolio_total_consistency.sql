with expected as (
  select valuation_date, portfolio_id, round(sum(market_value_eur), 2) as total
  from {{ ref('int_position_valuation') }} group by valuation_date, portfolio_id
)
select p.* from {{ ref('fct_portfolio_daily') }} p
full outer join expected e using (valuation_date, portfolio_id)
where p.total_value_eur is null or e.total is null or abs(p.total_value_eur - e.total) > 0.01
