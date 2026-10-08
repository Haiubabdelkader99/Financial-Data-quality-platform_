-- Every input holding must survive enrichment once, including missing references.
select 1 as failure
where (select count(*) from {{ ref('stg_positions') }})
   <> (select count(*) from {{ ref('int_position_valuation') }})
