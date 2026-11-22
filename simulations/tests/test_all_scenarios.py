import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "simulations"))

from scenario_engine import evaluate_case

DATA = ROOT / "simulations/data/scenario_cases.json"

with DATA.open(encoding="utf-8") as f:
    CASES = json.load(f)


class TestAllScenarios(unittest.TestCase):
    pass


def create_test(case, should_pass):
    def test(self):
        sample = json.loads(json.dumps(case))

        if not should_pass:
            for control in sample["required_controls"]:
                sample["controls"][control] = False

        result = evaluate_case(sample)

        expected = "PASS" if should_pass else "BLOCK"
        self.assertEqual(result["decision"], expected)

        if not should_pass:
            self.assertTrue(result["issues"])

    return test


for case in CASES:
    sid = case["scenario_id"].lower()

    setattr(
        TestAllScenarios,
        f"test_{sid}_control_passes",
        create_test(case, True)
    )

    setattr(
        TestAllScenarios,
        f"test_{sid}_failure_is_blocked",
        create_test(case, False)
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
