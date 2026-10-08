select * from {{ ref('fct_reconciliation') }}
where reconciliation_status <> 'MATCH'
order by valuation_date, portfolio_id
