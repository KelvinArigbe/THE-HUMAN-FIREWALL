import json
from pathlib import Path

from fraud_detection import (
    detect_beneficiary_mismatch,
    detect_duplicate_payments
)

BASE = Path(__file__).parent
DATA = BASE / "data"
REPORT = BASE / "reports" / "fraud-detection-results.json"

with (DATA / "transactions.json").open(encoding="utf-8") as file:
    transactions = json.load(file)

with (DATA / "customer_records.json").open(encoding="utf-8") as file:
    customers = json.load(file)

results = {
    "beneficiary_checks": [
        detect_beneficiary_mismatch(tx, customers)
        for tx in transactions
    ],
    "duplicate_checks": detect_duplicate_payments(transactions)
}

REPORT.parent.mkdir(parents=True, exist_ok=True)
with REPORT.open("w", encoding="utf-8") as file:
    json.dump(results, file, indent=2)

print("\nTHE HUMAN FIREWALL — FRAUD DETECTION")
print("=" * 48)

for category, checks in results.items():
    print(f"\n{category.upper().replace('_', ' ')}")
    for result in checks:
        print(
            f"{result['transaction_id']} | "
            f"{result['decision']} | {result['finding']}"
        )

print(f"\nReport saved to: {REPORT}")
