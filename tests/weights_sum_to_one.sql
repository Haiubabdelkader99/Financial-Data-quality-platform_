select valuation_date, portfolio_id, sum(weight) as total_weight
from {{ ref('fct_concentration') }}
group by valuation_date, portfolio_id
having abs(sum(weight) - 1) > 0.00001 or count(weight) <> count(*)
