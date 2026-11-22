import json
from pathlib import Path

BASE_DIR = Path(__file__).parent

TRANSACTIONS_FILE = BASE_DIR / "data" / "transactions.json"
CUSTOMERS_FILE = BASE_DIR / "data" / "customer_records.json"

REQUIRED_APPROVALS = {
    "low": ["account_officer"],
    "medium": ["account_officer", "group_head"],
    "high": ["account_officer", "group_head", "divisional_head"]
}


def validate_transaction(transaction, customer_records):
    issues = []

    customer_name = transaction.get("customer")
    customer = customer_records.get(customer_name)

    if customer is None:
        issues.append("Customer record not found")
    else:
        if customer.get("status") != "active":
            issues.append("Customer account is not active")

        if transaction.get("signatory") != customer.get("approved_signatory"):
            issues.append("Signatory mismatch")

        if transaction.get("beneficiary") != customer.get("approved_beneficiary"):
            issues.append("Beneficiary mismatch")

    if transaction.get("document_valid") is not True:
        issues.append("Document validation failed")

    if transaction.get("customer_confirmed") is not True:
        issues.append("Customer authorisation not confirmed")

    risk_level = transaction.get("risk_level")
    required = REQUIRED_APPROVALS.get(risk_level)

    if required is None:
        issues.append("Unknown risk level")
    else:
        approvals = transaction.get("approvals", {})

        for role in required:
            if approvals.get(role) is not True:
                issues.append(f"Missing approval: {role}")

    return {
        "transaction_id": transaction.get("transaction_id"),
        "decision": "BLOCK" if issues else "APPROVE",
        "issues": issues
    }


def main():
    with TRANSACTIONS_FILE.open("r", encoding="utf-8") as file:
        transactions = json.load(file)

    with CUSTOMERS_FILE.open("r", encoding="utf-8") as file:
        customer_records = json.load(file)

    print("\nTHE HUMAN FIREWALL — S01 VALIDATION ENGINE")
    print("=" * 48)

    for transaction in transactions:
        result = validate_transaction(transaction, customer_records)

        print(f"\nTransaction: {result['transaction_id']}")
        print(f"Decision: {result['decision']}")

        for issue in result["issues"]:
            print(f"  - {issue}")

        if not result["issues"]:
            print("  All simulated controls passed.")


if __name__ == "__main__":
    main()
