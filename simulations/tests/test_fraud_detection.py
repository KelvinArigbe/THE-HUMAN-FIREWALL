import json
import unittest
from pathlib import Path

from simulations.fraud_detection import (
    detect_beneficiary_mismatch,
    detect_duplicate_payments
)

DATA = Path(__file__).parents[1] / "data"


class FraudDetectionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with (DATA / "transactions.json").open(encoding="utf-8") as file:
            cls.transactions = json.load(file)

        with (DATA / "customer_records.json").open(encoding="utf-8") as file:
            cls.customers = json.load(file)

    def test_approved_beneficiary_passes(self):
        result = detect_beneficiary_mismatch(
            self.transactions[0], self.customers
        )
        self.assertEqual(result["decision"], "PASS")

    def test_altered_beneficiary_is_blocked(self):
        result = detect_beneficiary_mismatch(
            self.transactions[1], self.customers
        )
        self.assertEqual(result["decision"], "BLOCK")

    def test_unknown_customer_is_blocked(self):
        transaction = {
            **self.transactions[0],
            "customer": "Unknown Synthetic Customer"
        }
        result = detect_beneficiary_mismatch(transaction, self.customers)
        self.assertEqual(result["decision"], "BLOCK")

    def test_matching_payment_fingerprint_requires_review(self):
        first = {
            "transaction_id": "TEST-001",
            "customer": "Meridian Trading Ltd.",
            "amount": 100000,
            "beneficiary": "Apex Supplies Ltd."
        }
        second = {
            **first,
            "transaction_id": "TEST-002"
        }

        results = detect_duplicate_payments([first, second])
        self.assertEqual([r["decision"] for r in results], ["REVIEW", "REVIEW"])

    def test_repeated_instruction_reference_is_blocked(self):
        first = {
            "transaction_id": "TEST-003",
            "instruction_reference": "REF-100",
            "customer": "Meridian Trading Ltd.",
            "amount": 100000,
            "beneficiary": "Apex Supplies Ltd."
        }
        second = {
            **first,
            "transaction_id": "TEST-004"
        }

        results = detect_duplicate_payments([first, second])
        self.assertEqual([r["decision"] for r in results], ["BLOCK", "BLOCK"])

    def test_different_amounts_are_not_flagged_as_duplicates(self):
        first = {
            "transaction_id": "TEST-005",
            "customer": "Meridian Trading Ltd.",
            "amount": 100000,
            "beneficiary": "Apex Supplies Ltd."
        }
        second = {
            **first,
            "transaction_id": "TEST-006",
            "amount": 200000
        }

        results = detect_duplicate_payments([first, second])
        self.assertEqual([r["decision"] for r in results], ["PASS", "PASS"])


if __name__ == "__main__":
    unittest.main()
