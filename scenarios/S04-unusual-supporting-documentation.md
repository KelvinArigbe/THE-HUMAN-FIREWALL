# S04 — Unusual Supporting Documentation

**Domain:** Document fraud
**Organisation:** Meridian Bank (fictional)

## Objective
Test the defensive control: `supporting_documents_valid`.

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
