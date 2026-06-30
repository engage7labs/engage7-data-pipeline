# MAP - Pipeline Repository

## Purpose

Deterministic research and ETL pipeline repository for longitudinal wearable data processing, modeling, notebooks, and reproducibility artifacts.

## Key Paths

- `src/` - ETL, modeling, and utility source code.
- `scripts/` - pipeline execution and orchestration commands.
- `notebooks/` - analysis notebooks.
- `config/` - participant and label configuration.
- `requirements/` - Python dependency sets.
- `tests/` - reproducibility, leakage, and consistency tests.
- `docs/` - pipeline-specific documentation.
- `data/`, `results/`, `dist/`, `provenance/` - generated or sensitive local artifacts; treat with care.

## Canonical Flows

- Run the documented pipeline commands only when the sprint targets pipeline work.
- Preserve deterministic seeds, stage ordering, and reproducibility claims.
- Keep raw data and generated artifacts out of publishable paths unless explicitly approved and anonymized.

## Explicit Approval Areas

- Raw data handling, participant config, label rules, imputation, normalization, model training/evaluation, leakage controls, reproducibility snapshots, and generated reports.
- Any file containing raw health data, raw exports, identifiers, dates, or private research records.

## Common Validation

- Existing pipeline tests relevant to the touched stage.
- Reproducibility or anti-leak tests when ETL/modeling behavior changes.
- Notebook execution only when the sprint requires it.

## Related Docs

- `README.md`
- `CANONICAL_ENTRYPOINTS.md`
- `pipeline_overview.md`
- `docs/`
- `../docs/AI_CONTEXT.md`
