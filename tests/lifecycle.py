"""Check service reuse, shutdown and preservation without opening a browser."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
import sys

REPO = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--runtime', required=True)
args = parser.parse_args()
runtime = Path(args.runtime).resolve()
state_path = runtime / 'sessions' / hashlib.sha256(str(REPO).encode()).hexdigest()[:16] / 'state.json'

def hashes():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (REPO / 'work').glob('*') if p.is_file()}

def action(*flags):
    subprocess.run([sys.executable, str(REPO / 'tools/classroom.py'),
                    '--runtime', str(runtime), *flags], check=True, timeout=65)

before = hashes()
try:
    action('--no-open')
    first = json.loads(state_path.read_text())['pid']
    action('--no-open')
    assert json.loads(state_path.read_text())['pid'] == first, 'Repeated start created another service'
    assert hashes() == before, 'Setup or start changed existing personal files'
finally:
    action('--stop')
assert not state_path.exists(), 'Shutdown left active session state'
assert hashes() == before, 'Shutdown changed existing personal files'
out = REPO / '.validation'
out.mkdir(exist_ok=True)
(out / 'lifecycle.json').write_text(json.dumps({
    'service_reuse': 'passed', 'shutdown': 'passed', 'work_preservation': 'passed',
    'platform': sys.platform, 'browser_opened': False}, indent=2), encoding='utf-8')
print('Service reuse, shutdown and personal-file preservation passed.')
