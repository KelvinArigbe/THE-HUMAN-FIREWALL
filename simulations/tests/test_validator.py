import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "simulations"))

from validator import validate_transaction

DATA_DIR = PROJECT_ROOT / "simulations" / "data"


class TestTransactionValidation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with (DATA_DIR / "transactions.json").open() as file:
            cls.transactions = json.load(file)

        with (DATA_DIR / "customer_records.json").open() as file:
            cls.customers = json.load(file)

    def test_valid_transaction_is_approved(self):
        result = validate_transaction(
            self.transactions[0], self.customers
        )
        self.assertEqual(result["decision"], "APPROVE")

    def test_beneficiary_mismatch_is_blocked(self):
        result = validate_transaction(
            self.transactions[1], self.customers
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("Beneficiary mismatch", result["issues"])

    def test_unconfirmed_instruction_is_blocked(self):
        result = validate_transaction(
            self.transactions[2], self.customers
        )
        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn(
            "Customer authorisation not confirmed",
            result["issues"]
        )

    def test_missing_divisional_approval_is_blocked(self):
        result = validate_transaction(
            self.transactions[2], self.customers
        )
        self.assertIn(
            "Missing approval: divisional_head",
            result["issues"]
        )

    def test_invalid_document_is_blocked(self):
        transaction = self.transactions[0].copy()
        transaction["document_valid"] = False

        result = validate_transaction(transaction, self.customers)

        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("Document validation failed", result["issues"])

    def test_unregistered_customer_is_blocked(self):
        transaction = self.transactions[0].copy()
        transaction["customer"] = "Unknown Company Ltd."

        result = validate_transaction(transaction, self.customers)

        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("Customer record not found", result["issues"])

    def test_signatory_mismatch_is_blocked(self):
        transaction = self.transactions[0].copy()
        transaction["signatory"] = "Unapproved Signatory"

        result = validate_transaction(transaction, self.customers)

        self.assertEqual(result["decision"], "BLOCK")
        self.assertIn("Signatory mismatch", result["issues"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
