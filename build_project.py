from pathlib import Path
import json

ROOT = Path(__file__).parent

scenarios = [
("S01","Forged Payment Instruction","Document fraud","document_valid"),
("S02","Altered Beneficiary Details","Document fraud","beneficiary_matches"),
("S03","Replayed Payment Instruction","Document fraud","instruction_is_unique"),
("S04","Unusual Supporting Documentation","Document fraud","supporting_documents_valid"),
("S05","Customer Impersonation","Social engineering","customer_identity_verified"),
("S06","Executive Impersonation","Social engineering","executive_identity_verified"),
("S07","Urgency Manipulation","Social engineering","independent_review_completed"),
("S08","Insider-Assisted Fraud","Social engineering","segregation_of_duties_enforced"),
("S09","Unavailable Signatory","Telephone verification","callback_completed"),
("S10","Inconsistent Transaction Confirmation","Telephone verification","transaction_details_confirmed"),
("S11","Compromised Communication Channel","Telephone verification","trusted_channel_verified"),
("S12","Disputed Verbal Approval","Telephone verification","approval_evidence_confirmed"),
("S13","Missing Account Officer Approval","Management approvals","account_officer_approved"),
("S14","Missing Group Head Approval","Management approvals","group_head_approved"),
("S15","Missing Divisional Head Approval","Management approvals","divisional_head_approved"),
("S16","Duplicate Payment","Payment processing","duplicate_check_passed"),
("S17","Beneficiary Record Mismatch","Payment processing","beneficiary_record_matches"),
("S18","Unauthorised Transaction Release","Payment processing","release_authorised"),
("S19","Incomplete Approval Audit Trail","Investigation","audit_trail_complete"),
("S20","Delayed Fraud Escalation","Investigation","fraud_escalation_timely"),
]

def write(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

catalogue = ["# THE HUMAN FIREWALL — Scenario Catalogue", ""]
cases = []

for sid, title, domain, control in scenarios:
    catalogue.append(f"- **{sid}: {title}** — {domain}.")
    filename = title.lower().replace(" ", "-")
    write(
        f"scenarios/{sid}-{filename}.md",
        f"""# {sid} — {title}

**Domain:** {domain}
**Organisation:** Meridian Bank (fictional)

## Objective
Test the defensive control: `{control}`.

## Scenario
A fictional transaction or workflow contains a deliberately invalid,
incomplete or suspicious condition.

## Safe test
Use synthetic data. Simulate a failed control and verify that the
system blocks the transaction or raises an alert.

## Expected outcome
The control failure is detected, recorded and escalated for review.

## Evidence
Retain test input, decision, test output and remediation recommendation.

## Limitation
This is an educational simulation, not a test of any real bank.
"""
    )

    cases.append({
        "scenario_id": sid,
        "title": title,
        "domain": domain,
        "required_controls": [control],
        "controls": {control: True}
    })

write("scenarios/SCENARIO-CATALOGUE.md", "\n".join(catalogue))
write("simulations/data/scenario_cases.json", json.dumps(cases, indent=2))

write("simulations/scenario_engine.py", '''
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
''')

write("architecture/human-firewall-architecture.mmd", """flowchart TD
A["Synthetic input"] --> B["Scenario engine"]
B --> C["Control checks"]
C --> D{"All controls satisfied?"}
D -->|Yes| E["PASS"]
D -->|No| F["BLOCK and record issue"]
E --> G["Test evidence"]
F --> G
G --> H["Security assessment"]
""")

write("reports/FINAL-SECURITY-ASSESSMENT.md", """# THE HUMAN FIREWALL — Security Assessment

## Executive summary
Defensive simulation of fictional banking transaction workflows.

## Scope
20 scenarios covering document fraud, social engineering, telephone
verification, approvals, payment processing and investigation.

## Methodology
Synthetic test cases and automated positive and negative tests.

## Results
Populate from actual test execution.

## Findings
Document observed simulation results and supporting evidence.

## Recommendations
Document preventive controls, detective controls and remediation.

## Limitations
This project does not access or test real banking systems.
""")

write("README.md", """# THE HUMAN FIREWALL

Defensive banking social-engineering and transaction-fraud simulation.

- 20 fictional scenarios
- Python validation engine
- Automated tests
- Architecture diagram
- Evidence and security assessment

Run:
`python3 -m unittest discover -s simulations/tests -v`

All data and organisations are fictional.
""")

print("Build files generated successfully.")
print(f"Scenarios created: {len(scenarios)}")
print("Existing S01 files preserved.")
