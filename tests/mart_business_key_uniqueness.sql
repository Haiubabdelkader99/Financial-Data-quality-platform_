select 'portfolio' as dataset, valuation_date, portfolio_id, count(*) as records
from {{ ref('fct_portfolio_daily') }} group by valuation_date, portfolio_id having count(*) > 1
union all
select 'reconciliation', valuation_date, portfolio_id, count(*)
from {{ ref('fct_reconciliation') }} group by valuation_date, portfolio_id having count(*) > 1
