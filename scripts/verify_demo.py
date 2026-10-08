"""Independent golden expectations for the supplied synthetic fixture."""
import os
from pathlib import Path
from decimal import Decimal
import duckdb

ROOT = Path(__file__).resolve().parents[1]
with duckdb.connect(os.environ.get('FINANCE_DB_PATH', str(ROOT / 'finance.duckdb')), read_only=True) as con:
    assert con.execute('select count(*) from int_position_valuation').fetchone()[0] == 18
    assert con.execute('select count(*) from fct_portfolio_daily').fetchone()[0] == 6
    actual = {(str(d), p): v for d, p, v in con.execute('select valuation_date, portfolio_id, total_value_eur from fct_portfolio_daily').fetchall()}
    expected = {
        ('2026-09-28', 'P001'): Decimal('26550.00'),
        ('2026-09-28', 'P002'): Decimal('38045.00'),
        ('2026-09-28', 'P003'): Decimal('49580.00'),
        ('2026-09-29', 'P001'): Decimal('26784.00'),
        ('2026-09-29', 'P002'): Decimal('38440.75'),
        ('2026-09-29', 'P003'): Decimal('49881.00'),
    }
    assert actual == expected, (actual, expected)
    exceptions = con.execute("select portfolio_id, difference_eur from fct_reconciliation where reconciliation_status <> 'MATCH'").fetchall()
    assert exceptions == [('P002', Decimal('-50.00'))], exceptions
    assert con.execute("select count(*) from fct_concentration where control_status = 'BREACH'").fetchone()[0] == 4
print('PASS: 18 positions, 6 portfolio-days, expected values, one EUR 50 break, 4 breaches.')
