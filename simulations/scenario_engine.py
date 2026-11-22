"""Defensive detection engine for The Human Firewall."""

RULES = {
    "S01": ("document_integrity_verified", "Payment instruction integrity could not be verified."),
    "S02": ("beneficiary_matches", "Beneficiary details differ from the approved record."),
    "S03": ("instruction_is_unique", "Payment instruction appears to have been replayed."),
    "S04": ("supporting_documents_valid", "Supporting documents failed validation."),
    "S05": ("customer_identity_verified", "Customer identity verification failed."),
    "S06": ("executive_identity_verified", "Executive identity or authority could not be verified."),
    "S07": ("independent_review_completed", "Urgency-related request lacks independent review."),
    "S08": ("segregation_of_duties_enforced", "Initiator and approver duties are not adequately separated."),
    "S09": ("callback_completed", "Required independent callback was not completed."),
    "S10": ("transaction_details_confirmed", "Transaction details were not independently confirmed."),
    "S11": ("trusted_channel_verified", "Communication channel could not be verified as trusted."),
    "S12": ("approval_evidence_confirmed", "Verbal approval lacks verifiable supporting evidence."),
    "S13": ("account_officer_approved", "Account Officer approval is missing."),
    "S14": ("group_head_approved", "Group Head approval is missing."),
    "S15": ("divisional_head_approved", "Divisional Head approval is missing."),
    "S16": ("duplicate_check_passed", "Duplicate payment check identified a potential duplicate."),
    "S17": ("beneficiary_record_matches", "Payment beneficiary does not match the verified beneficiary record."),
    "S18": ("release_authorised", "Transaction release lacks recorded authorisation."),
    "S19": ("audit_trail_complete", "Approval or transaction audit trail is incomplete."),
    "S20": ("fraud_escalation_timely", "Fraud concern was not escalated within the defined timeframe."),
}


def evaluate_case(case):
    scenario_id = case.get("scenario_id", "UNKNOWN")
    findings = []

    if scenario_id not in RULES:
        findings.append("Unknown scenario identifier.")
    else:
        control, message = RULES[scenario_id]
        if case.get("signals", {}).get(control) is not True:
            findings.append(message)

    return {
        "scenario_id": scenario_id,
        "title": case.get("title", "Untitled scenario"),
        "decision": "BLOCK" if findings else "PASS",
        "findings": findings,
        "risk_level": "HIGH" if findings else "LOW",
    }


def evaluate_all(cases):
    return [evaluate_case(case) for case in cases]
