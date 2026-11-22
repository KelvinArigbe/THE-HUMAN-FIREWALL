import json
import unittest
from pathlib import Path

from simulations.scenario_engine import RULES, evaluate_case

DATA_FILE = Path(__file__).parents[1] / "data" / "scenario_cases.json"


class TestAllScenarios(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with DATA_FILE.open(encoding="utf-8") as file:
            cls.cases = json.load(file)

    def test_all_twenty_scenarios_are_present(self):
        ids = {case["scenario_id"] for case in self.cases}
        self.assertEqual(ids, set(RULES))

    def test_s01_to_s20_baseline_cases_pass(self):
        for case in self.cases:
            with self.subTest(scenario=case["scenario_id"]):
                result = evaluate_case(case)
                self.assertEqual(result["decision"], "PASS")

    def test_s01_to_s20_failed_controls_are_blocked(self):
        for case in self.cases:
            scenario_id = case["scenario_id"]
            control, _ = RULES[scenario_id]

            failing_case = {
                **case,
                "signals": {**case["signals"], control: False}
            }

            with self.subTest(scenario=scenario_id):
                result = evaluate_case(failing_case)
                self.assertEqual(result["decision"], "BLOCK")
                self.assertTrue(result["findings"])

    def test_every_case_has_required_metadata(self):
        for case in self.cases:
            with self.subTest(scenario=case["scenario_id"]):
                self.assertIn("title", case)
                self.assertIn("domain", case)
                self.assertIn("signals", case)


if __name__ == "__main__":
    unittest.main()
