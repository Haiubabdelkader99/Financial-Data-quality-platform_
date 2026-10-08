"""Cross-platform runner. Build failures prevent publication of a new report."""
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    executable = shutil.which('dbt')
    if not executable:
        raise SystemExit('dbt not found. Activate .venv and install requirements.txt.')
    env = os.environ.copy()
    env['FINANCE_DB_PATH'] = str(ROOT / 'finance.duckdb')
    env['DBT_SEND_ANONYMOUS_USAGE_STATS'] = 'false'
    # Remove old reports so a failed build cannot look like a fresh successful run.
    output = ROOT / 'outputs'
    if output.exists():
        shutil.rmtree(output)
    subprocess.run([executable, 'build', '--profiles-dir', str(ROOT)],
                   cwd=ROOT, env=env, check=True)
    # docs generate rewrites run_results.json; preserve the tested build evidence.
    shutil.copy2(ROOT / 'target' / 'run_results.json', ROOT / 'target' / 'build_run_results.json')
    subprocess.run([executable, 'docs', 'generate', '--profiles-dir', str(ROOT)],
                   cwd=ROOT, env=env, check=True)
    subprocess.run([sys.executable, str(ROOT / 'scripts' / 'export_report.py')],
                   cwd=ROOT, env=env, check=True)

if __name__ == '__main__':
    main()
