"""Evidence-based defensive checks using synthetic transaction records."""

from collections import defaultdict


def detect_beneficiary_mismatch(transaction, customer_records):
    customer_name = transaction.get("customer")
    customer = customer_records.get(customer_name)

    if customer is None:
        return {
            "scenario_ids": ["S02", "S17"],
            "transaction_id": transaction.get("transaction_id"),
            "decision": "BLOCK",
            "finding": "Customer record not found; beneficiary cannot be verified."
        }

    submitted = transaction.get("beneficiary", "")
    approved = customer.get("approved_beneficiary", "")

    if submitted.strip().casefold() != approved.strip().casefold():
        return {
            "scenario_ids": ["S02", "S17"],
            "transaction_id": transaction.get("transaction_id"),
            "decision": "BLOCK",
            "finding": "Submitted beneficiary differs from the approved customer record."
        }

    return {
        "scenario_ids": ["S02", "S17"],
        "transaction_id": transaction.get("transaction_id"),
        "decision": "PASS",
        "finding": "Beneficiary matches the approved customer record."
    }


def detect_duplicate_payments(transactions):
    """
    Exact repeated instruction references are blocked.
    Matching customer/amount/beneficiary combinations are flagged for review.

    The fingerprint is a screening heuristic, not proof of fraud.
    """

    reference_groups = defaultdict(list)
    fingerprint_groups = defaultdict(list)

    for transaction in transactions:
        transaction_id = transaction.get("transaction_id", "UNKNOWN")
        reference = transaction.get("instruction_reference")

        if reference:
            reference_groups[str(reference).strip().casefold()].append(transaction_id)

        fingerprint = (
            str(transaction.get("customer", "")).strip().casefold(),
            transaction.get("amount"),
            str(transaction.get("beneficiary", "")).strip().casefold(),
            str(transaction.get("currency", "")).strip().casefold(),
            str(transaction.get("payment_date", "")).strip()
        )
        fingerprint_groups[fingerprint].append(transaction_id)

    results = []

    for transaction in transactions:
        transaction_id = transaction.get("transaction_id", "UNKNOWN")
        reference = transaction.get("instruction_reference")

        fingerprint = (
            str(transaction.get("customer", "")).strip().casefold(),
            transaction.get("amount"),
            str(transaction.get("beneficiary", "")).strip().casefold(),
            str(transaction.get("currency", "")).strip().casefold(),
            str(transaction.get("payment_date", "")).strip()
        )

        repeated_reference = (
            reference
            and len(reference_groups[str(reference).strip().casefold()]) > 1
        )

        repeated_fingerprint = len(fingerprint_groups[fingerprint]) > 1

        if repeated_reference:
            decision = "BLOCK"
            finding = "Repeated payment instruction reference detected."
        elif repeated_fingerprint:
            decision = "REVIEW"
            finding = (
                "Potential duplicate: customer, amount and beneficiary "
                "match another transaction. Manual review required."
            )
        else:
            decision = "PASS"
            finding = "No duplicate indicator detected."

        results.append({
            "scenario_ids": ["S03", "S16"],
            "transaction_id": transaction_id,
            "decision": decision,
            "finding": finding
        })

    return results
