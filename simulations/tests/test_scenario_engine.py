import unittest
from simulations.scenario_engine import RULES, evaluate_case


class ScenarioEngineTests(unittest.TestCase):

    def test_all_twenty_scenarios_have_rules(self):
        self.assertEqual(len(RULES), 20)
        self.assertEqual(set(RULES), {f"S{i:02d}" for i in range(1, 21)})

    def test_each_scenario_passes_when_its_control_is_verified(self):
        for scenario_id, (control, _) in RULES.items():
            with self.subTest(scenario=scenario_id):
                result = evaluate_case({
                    "scenario_id": scenario_id,
                    "signals": {control: True}
                })
                self.assertEqual(result["decision"], "PASS")
                self.assertEqual(result["findings"], [])

    def test_each_scenario_blocks_when_its_control_fails(self):
        for scenario_id, (control, _) in RULES.items():
            with self.subTest(scenario=scenario_id):
                result = evaluate_case({
                    "scenario_id": scenario_id,
                    "signals": {control: False}
                })
                self.assertEqual(result["decision"], "BLOCK")
                self.assertEqual(len(result["findings"]), 1)

    def test_missing_control_is_blocked(self):
        for scenario_id in RULES:
            with self.subTest(scenario=scenario_id):
                result = evaluate_case({"scenario_id": scenario_id})
                self.assertEqual(result["decision"], "BLOCK")

    def test_unknown_scenario_is_blocked(self):
        result = evaluate_case({"scenario_id": "S99"})
        self.assertEqual(result["decision"], "BLOCK")

    def test_result_contains_risk_level(self):
        result = evaluate_case({
            "scenario_id": "S02",
            "signals": {"beneficiary_matches": False}
        })
        self.assertEqual(result["risk_level"], "HIGH")


if __name__ == "__main__":
    unittest.main()
