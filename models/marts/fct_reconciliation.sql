-- Full outer join exposes missing portfolios/dates on either side.
with joined as (
    select coalesce(p.valuation_date, cast(c.valuation_date as date)) as valuation_date,
           coalesce(p.portfolio_id, c.portfolio_id) as portfolio_id,
           p.total_value_eur as calculated_value_eur,
           cast(c.reported_value_eur as decimal(20, 2)) as reported_value_eur
    from {{ ref('fct_portfolio_daily') }} p
    full outer join {{ ref('custodian_totals') }} c
      on p.portfolio_id = c.portfolio_id
     and p.valuation_date = cast(c.valuation_date as date)
), differences as (
    select *, calculated_value_eur - reported_value_eur as difference_eur
    from joined
)
select *, cast(1.00 as decimal(20, 2)) as tolerance_eur,
       case
         when calculated_value_eur is null then 'MISSING_INTERNAL'
         when reported_value_eur is null then 'MISSING_CUSTODIAN'
         when abs(difference_eur) <= 1.00 then 'MATCH'
         else 'BREAK'
       end as reconciliation_status
from differences
