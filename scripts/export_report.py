"""Exports control results and a portable HTML report from a tested local build."""
import csv
import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import duckdb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs'

def export(con, table):
    cursor = con.execute(f'SELECT * FROM {table} ORDER BY valuation_date, portfolio_id')
    columns = [item[0] for item in cursor.description]
    records = cursor.fetchall()
    with (OUT / f'{table}.csv').open('w', newline='', encoding='utf-8') as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(records)
    return columns, records

def html_table(columns, records):
    head = ''.join('<th>' + html.escape(c) + '</th>' for c in columns)
    rows = ''.join('<tr>' + ''.join('<td>' + html.escape(str(v)) + '</td>' for v in row)
                   + '</tr>' for row in records)
    return '<div class="scroll"><table><thead><tr>' + head + '</tr></thead><tbody>' + rows + '</tbody></table></div>'

def main():
    OUT.mkdir(exist_ok=True)
    with duckdb.connect(os.environ.get('FINANCE_DB_PATH', str(ROOT / 'finance.duckdb')), read_only=True) as con:
        portfolio = export(con, 'fct_portfolio_daily')
        recon = export(con, 'fct_reconciliation')
        concentration = export(con, 'fct_concentration')
        breaks = con.execute("select * from fct_reconciliation where reconciliation_status <> 'MATCH' order by valuation_date, portfolio_id").fetchall()
        breach_rows = con.execute("select * from fct_concentration where control_status = 'BREACH' order by valuation_date, portfolio_id").fetchall()
    summary = {
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'data_classification': 'SYNTHETIC',
        'portfolio_days': len(portfolio[1]),
        'reconciliation_exceptions': len(breaks),
        'concentration_breaches': len(breach_rows),
        'alert_state': 'REVIEW_REQUIRED' if breaks or breach_rows else 'OK',
        'note': 'Local alert artifact only; no email or external notification is sent.'
    }
    (OUT / 'alerts.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    page = '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Financial Data Quality</title>'
    page += '<style>body{font:15px system-ui;background:#f3f6fa;color:#14253d;max-width:1200px;margin:40px auto;padding:0 24px}h1{font-size:34px}h2{margin-top:32px}.cards{display:flex;flex-wrap:wrap;gap:18px}.card{background:white;padding:20px;border-radius:12px;flex:1;min-width:180px}.number{font-size:32px;font-weight:700}.scroll{overflow:auto}table{border-collapse:collapse;width:100%;background:white;font-size:13px}th,td{padding:10px;border-bottom:1px solid #ddd;text-align:left}th{background:#16385c;color:white}.note{color:#52657e}</style>'
    page += '<h1>Financial Data Quality Platform</h1><p class="note">Synthetic portfolio reporting · dbt + DuckDB + Python · EUR values</p><div class="cards">'
    for title, value in [('Portfolio-days', summary['portfolio_days']), ('Reconciliation exceptions', len(breaks)), ('Concentration breaches', len(breach_rows))]:
        page += f'<div class="card">{title}<div class="number">{value}</div></div>'
    page += '</div><h2>Portfolio valuation</h2>' + html_table(*portfolio)
    page += '<h2>Reconciliation exceptions</h2>' + html_table(recon[0], breaks)
    page += '<h2>Concentration breaches</h2>' + html_table(concentration[0], breach_rows)
    page += '<p class="note">Holdings value is not NAV. Concentration thresholds are illustrative, not regulatory. Source dates: 28–29 September 2026. Generated: ' + html.escape(summary['generated_at_utc']) + '</p></html>'
    (OUT / 'report.html').write_text(page, encoding='utf-8')
    print(json.dumps(summary, indent=2))
    print('Open outputs/report.html in your browser.')

if __name__ == '__main__':
    main()
