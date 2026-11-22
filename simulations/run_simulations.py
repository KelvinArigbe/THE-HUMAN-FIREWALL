import json
from pathlib import Path
from scenario_engine import evaluate_all

BASE = Path(__file__).parent
DATA = BASE / "data" / "scenario_cases.json"
REPORT = BASE / "reports" / "detection-results.json"

with DATA.open(encoding="utf-8") as f:
    cases = json.load(f)

results = evaluate_all(cases)

REPORT.parent.mkdir(parents=True, exist_ok=True)
with REPORT.open("w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nTHE HUMAN FIREWALL — DETECTION ENGINE")
print("=" * 48)

for result in results:
    print(f"\n{result['scenario_id']} | {result['title']}")
    print(f"Decision: {result['decision']} | Risk: {result['risk_level']}")
    for finding in result["findings"]:
        print(f"  ALERT: {finding}")

print(f"\nTotal scenarios: {len(results)}")
print(f"Blocked: {sum(r['decision'] == 'BLOCK' for r in results)}")
print(f"Passed: {sum(r['decision'] == 'PASS' for r in results)}")
print(f"Report saved: {REPORT}")
