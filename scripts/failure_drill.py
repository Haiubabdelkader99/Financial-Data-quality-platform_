"""Negative integration tests in temporary copies; never changes the working seeds."""
import csv
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def mutate(path, scenario):
    with path.open(newline='', encoding='utf-8') as handle:
        reader = csv.DictReader(handle)
        fields, rows = reader.fieldnames, list(reader)
    if scenario == 'duplicate':
        rows.append(rows[0].copy())
    elif scenario == 'missing_fx':
        rows = [r for r in rows if not (r['currency'] == 'USD' and r['valuation_date'] == '2026-09-29')]
    elif scenario == 'unknown_instrument':
        rows[0]['instrument_id'] = 'UNKNOWN'
    with path.open('w', newline='', encoding='utf-8') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def main():
    executable = shutil.which('dbt')
    if not executable:
        raise SystemExit('Activate .venv and install requirements.txt first.')
    scenarios = [('duplicate', 'positions.csv', 'unique_stg_positions_position_id'),
                 ('missing_fx', 'fx_rates.csv', 'not_null_int_position_valuation_market_value_eur'),
                 ('unknown_instrument', 'positions.csv', 'relationships_stg_positions_instrument_id')]
    for name, filename, test_prefix in scenarios:
        with tempfile.TemporaryDirectory(prefix='finance-drill-') as temp:
            case = Path(temp) / 'project'
            shutil.copytree(ROOT, case, ignore=shutil.ignore_patterns('.venv', '.git', 'target', 'logs', 'outputs', '__pycache__', '*.duckdb*'))
            mutate(case / 'seeds' / filename, name)
            env = os.environ.copy()
            env['FINANCE_DB_PATH'] = str(case / 'finance.duckdb')
            env['DBT_SEND_ANONYMOUS_USAGE_STATS'] = 'false'
            result = subprocess.run([executable, 'build', '--profiles-dir', str(case)], cwd=case,
                                    env=env, capture_output=True, text=True)
            artifact = case / 'target' / 'run_results.json'
            if not artifact.exists():
                raise RuntimeError(result.stdout + result.stderr)
            results = json.loads(artifact.read_text())['results']
            detected = any(r['status'] == 'fail' and test_prefix in r['unique_id'] for r in results)
            if result.returncode == 0 or not detected:
                raise AssertionError(f'{name}: expected specific data test to fail\n' + result.stdout + result.stderr)
            print(f'PASS: {name} detected by {test_prefix}; build blocked.')

if __name__ == '__main__':
    main()
