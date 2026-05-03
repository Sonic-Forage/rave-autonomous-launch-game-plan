#!/usr/bin/env python3
from pathlib import Path
import json, sys
ROOT = Path(__file__).resolve().parents[1]
FIELD = Path('/opt/data/workspace/projects/rave-culture-field-guide')
required = [
    ROOT/'docs/planning/TONIGHT_AUTONOMOUS_LAUNCH_PLAN.md',
    ROOT/'docs/planning/AUTONOMOUS_TASK_BOARD.md',
    ROOT/'docs/reports/VIDEO_RELEASE_PREP.md',
    ROOT/'docs/reports/HUMAN_APPROVAL_DECISION_LEDGER.md',
    ROOT/'docs/reports/LAUNCH_PROOF_INDEX.md',
    ROOT/'site/data/human-approval-decision-ledger.json',
    ROOT/'site/data/launch-proof-index.json',
    FIELD/'CONTRIBUTING.md',
    FIELD/'.github/ISSUE_TEMPLATE/city_chapter.yml',
    FIELD/'docs/community/CITY_CHAPTER_TEMPLATE.md',
]
errors=[]
for p in required:
    if not p.exists():
        errors.append(f'missing: {p}')
ledger=json.loads((ROOT/'site/data/human-approval-decision-ledger.json').read_text())
if ledger.get('status')!='closed_until_human_yes':
    errors.append('approval ledger not closed')
if len(ledger.get('decision_slots',[])) < 5:
    errors.append('approval ledger needs at least five decision slots')
for slot in ledger.get('decision_slots',[]):
    if slot.get('default_state')!='closed_until_human_yes':
        errors.append(f"slot not closed: {slot.get('id')}")
proof=json.loads((ROOT/'site/data/launch-proof-index.json').read_text())
if not proof.get('requires_human_approval'):
    errors.append('proof index must require human approval')
for k,v in proof.get('risky_flags',{}).items():
    if v is not False:
        errors.append(f'risky flag open: {k}')
for item in proof.get('proof_claims',[]):
    for pr in item.get('proof',[]):
        if pr.startswith('/opt/data/') and not Path(pr).exists():
            errors.append(f'proof path missing: {pr}')
video=(ROOT/'docs/reports/VIDEO_RELEASE_PREP.md').read_text(errors='replace')
for s in ['60-second launch video script','90-second launch video script','3-minute demo recording run-of-show','do not post autonomously']:
    if s.lower() not in video.lower():
        errors.append(f'video prep missing: {s}')
plan=(ROOT/'docs/planning/TONIGHT_AUTONOMOUS_LAUNCH_PLAN.md').read_text(errors='replace')
for s in ['Sonic-Forage','02:00','04:20','11:11','Closed-by-default']:
    if s not in plan:
        errors.append(f'plan missing: {s}')
if errors:
    print('TONIGHT LAUNCH VERIFY FAILED')
    for e in errors: print('-', e)
    sys.exit(1)
print('TONIGHT LAUNCH VERIFY OK')
print(f'root: {ROOT}')
print(f'proof claims: {len(proof.get("proof_claims", []))}')
print(f'decision slots: {len(ledger.get("decision_slots", []))}')
