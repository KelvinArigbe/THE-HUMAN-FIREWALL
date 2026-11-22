
def evaluate_case(case):
    issues = []
    required = case.get("required_controls", [])

    if not required:
        issues.append("No control requirements defined")

    for control in required:
        if case.get("controls", {}).get(control) is not True:
            issues.append(f"Control failed: {control}")

    return {
        "scenario_id": case.get("scenario_id", "UNKNOWN"),
        "decision": "BLOCK" if issues else "PASS",
        "issues": issues
    }
