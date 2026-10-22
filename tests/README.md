# Tests and QA checks

## Synthetic CI checks

`PYTHONPATH=src python -m pytest -q tests/test_io_guards.py tests/test_release_guard.py` checks CSV replacement,
backup preservation, non-writing dry runs and failure preservation using only
synthetic DataFrames and temporary directories. It needs pytest and pandas, not
the full ML stack, participant fixtures or credentials. GitHub Actions executes
these checks on Ubuntu 24.04 and 26.04. This is not timezone/CLI or end-to-end ETL
coverage and does not replace the domain audits described below. Release-guard
tests use isolated temporary git repositories to verify no-tag skipping, valid
metadata resolution and rejection of missing notes, without publishing anything.

## Legacy pytest suite (v4.2+)

## Status: ⚠️ Legacy pytest tests removed

This directory previously contained pytest-based unit tests created during exploratory model implementation (v4.0–4.1).

## Current QA Strategy (v4.2+)

Data-dependent pipeline validation uses a **domain-specific ETL audit system**;
the synthetic CI unit tests above complement it.

### ETL Audit Module

- **File:** `src/etl/etl_audit.py` (~1,874 lines)
- **Purpose:** PhD-level regression testing for data integrity
- **Domains:** cardio, activity, sleep, meds, som, unified_ext, labels

### Usage

```bash
# Individual domain audits
make qc-cardio PID=P000001 SNAPSHOT=2025-11-07
make qc-activity PID=P000001 SNAPSHOT=2025-11-07
make qc-sleep PID=P000001 SNAPSHOT=2025-11-07

# Run all audits
make qc-all PID=P000001 SNAPSHOT=2025-11-07
```

### Outputs

- **CSV:** `data/etl/<PID>/<SNAPSHOT>/qc/<domain>_audit.csv`
- **JSON:** `data/etl/<PID>/<SNAPSHOT>/qc/<domain>_audit.json`
- **Markdown:** `docs/reports/qc/QC_<domain>_<PID>_<SNAPSHOT>.md`

### Exit Codes

- `0` = PASS (all checks passed)
- `1` = FAIL (critical issues found)

### Why domain audits for pipeline data?

1. **Domain-specific:** ETL audits are tailored to physiological data QC
2. **Integrated:** Audits run as part of pipeline workflow
3. **Provenance:** Generates scientific-grade QC reports automatically
4. **Reproducibility:** PhD-level traceability for academic rigor

## Historical Context

Deleted tests (v4.3.2 cleanup):

- `test_canonical_pbsi_integration.py` → Superseded by `make qc-labels`
- `test_cardio_sleep_cli.py` → Superseded by `make qc-cardio`, `make qc-sleep`
- `test_enrich_global.py` → Superseded by `make qc-unified-ext`
- `test_zepp_*_loader.py` → Integration tested in production
- `idempotence_a6_a7_a8.py` → Replaced by provenance SHA256 tracking

See `docs/copilot/TESTS_CLEANUP_AUDIT.md` for full analysis.
