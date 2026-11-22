# THE HUMAN FIREWALL
### Banking Social Engineering & Transaction Fraud Simulation

## Overview
The Human Firewall is a defensive cybersecurity portfolio project
examining social engineering and transaction fraud risks in fictional
banking payment workflows.

It uses synthetic customer records, simulated transactions and Python
validation logic to demonstrate how preventive and detective controls
can be evaluated.

## Project Scope

20 scenarios across six domains:

1. Document and payment instruction fraud
2. Social engineering and impersonation
3. Telephone verification
4. Management approval controls
5. Payment processing
6. Investigation and accountability

## Technology
- Python 3
- JSON
- unittest
- Mermaid diagrams
- SHA-256 evidence integrity checks

## Run the simulations

Original S01 validation:

    python3 simulations/validator.py

Complete automated test suite:

    python3 -m unittest discover -s simulations/tests -v

## Test Results

The recorded test run contains 47 passing tests:
- 7 tests for the original S01 transaction validator.
- 40 generic scenario-engine tests covering pass/block behaviour.

The 40 generated tests are not independent simulations of 20 distinct
fraud mechanisms. Further scenario-specific implementation is required.

## Architecture

See `architecture/human-firewall-architecture.mmd`.

## Evidence

See `evidence/S01/` and `evidence/PROJECT/`.

## Security and Ethical Scope

All organisations, identities, customer records and transactions are
fictional. No real banking systems, accounts, credentials or payment
channels are accessed or tested.

This project evaluates an educational defensive control model. It does
not claim to establish the effectiveness of any real bank's controls.

## Author
Kelvin Arigbe
