#!/usr/bin/env python3
from pathlib import Path
import json, sys, re
ROOT=Path(__file__).resolve().parents[1]
required=[
 'README.md','docs/launch/GAME_PLAN.md','docs/proof/WHAT_WE_DID.md','docs/operator/DEMO_RUNBOOK.md','site/index.html','site/data/launch-manifest.json','LICENSE'
]
errors=[]
for rel in required:
    p=ROOT/rel
    if not p.exists() or p.stat().st_size == 0:
        errors.append(f'missing or empty: {rel}')
try:
    m=json.loads((ROOT/'site/data/launch-manifest.json').read_text())
    gates=m.get('closed_gates',{})
    risky=['outreach_sent','payment_link_created','gpu_or_training_job_started','private_media_uploaded','voice_to_shell_enabled']
    for k in risky:
        if gates.get(k) is not False:
            errors.append(f'closed gate not false: {k}')
    if gates.get('requires_human_approval_for_next_launch_step') is not True:
        errors.append('human approval flag must be true')
    if 'rave-culture-field-guide' not in json.dumps(m):
        errors.append('manifest missing companion repo reference')
except Exception as e:
    errors.append(f'manifest invalid: {e}')

all_text='\n'.join(
    p.read_text(errors='replace')
    for p in ROOT.rglob('*')
    if p.is_file()
    and p.suffix.lower() in {'.md','.html','.json'}
)
required_phrases=['human approval','rave-culture-field-guide','RAVE Act','closed']
for phrase in required_phrases:
    if phrase.lower() not in all_text.lower():
        errors.append(f'missing phrase: {phrase}')
# Detect positive launch overclaims while allowing explicit non-claim safety copy.
positive_overclaim_patterns = [
    r'(?<!not prove )revenue was earned',
    r'(?<!not claim )revenue earned',
    r'(?<!no )payment link was created',
    r'(?<!no )gpu job was started',
    r'(?<!does not prove a )model was trained',
]
for pattern in positive_overclaim_patterns:
    if re.search(pattern, all_text, flags=re.IGNORECASE):
        errors.append(f'unsafe positive overclaim pattern present: {pattern}')
if errors:
    print('VERIFY FAILED')
    for e in errors: print('-',e)
    sys.exit(1)
print('VERIFY OK')
print(f'root: {ROOT}')
print(f'required files: {len(required)}')
