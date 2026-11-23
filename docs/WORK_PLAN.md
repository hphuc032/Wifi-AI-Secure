# Team work plan — Wifi-AI Secure

## 1. Ownership and boundaries

| Member | Owner | Main deliverables | Owns these paths |
|---|---|---|---|
| Data | Hoàng Phúc | AWID3 inventory, data validation, cleaning, preprocessing pipeline, feature schema, reproducible split | `data/`, `src/data/`, `configs/data/`, `tests/data/`, `docs/data/` |
| AI | Quốc Đạt | Baseline models, training scripts, model evaluation, inference wrapper, model cards | `src/models/`, `src/training/`, `src/evaluation/`, `models/README.md`, `tests/models/`, `docs/ai/` |
| App | Tiến Đạt | FastAPI service, persistence, alert workflow, dashboard, application integration | `src/api/`, `src/app/`, `src/database/`, `src/alerts/`, `tests/api/`, `docs/app/` |

All members: review interface changes, write tests for their module, update documentation, and participate in integration and demo.

## 2. Parallel schedule (8 weeks)

| Week | Hoàng Phúc — Data | Quốc Đạt — AI | Tiến Đạt — App | Integration checkpoint |
|---|---|---|---|---|
| 1 | Obtain AWID3; inventory files, labels, columns, data license/terms; profile missing/invalid values | Set up ML environment; inspect feature/label contract; build baseline training skeleton using synthetic fixture | Set up app skeleton, API contract stubs, dashboard wireframe, SQLite schema draft | Agree schema, label mapping, output contract, Python version and dependency policy |
| 2 | Implement parser/loader and data quality report | Implement baseline Random Forest and evaluation skeleton against fixture | Implement API endpoints with mock predictor; build dashboard navigation | All three modules run independently using shared fixtures |
| 3 | Implement cleaning and preprocessing; document transformations | Train first baseline using approved processed sample; save metrics and config | Persist detection events; show mock/live event history | First end-to-end path with mock prediction |
| 4 | Implement leakage-aware train/validation/test split and feature selection | Add XGBoost and FeedForward experiments; track parameters | Add detection result view and alert status flow | Replace mock data path with processed AWID3 pipeline |
| 5 | Validate data quality, class balance and split reproducibility | Evaluate per-class precision/recall/F1, macro-F1, confusion matrix; assess class imbalance | Add model metrics page and filtering | Review false positives/false negatives and latency |
| 6 | Freeze preprocessing interface and version metadata | Package inference interface and model artifacts/metadata | Integrate model inference with API and dashboard | Full local system using held-out test data |
| 7 | Fix data edge cases; reproduce pipeline | Tune models; compare models; document limitations | Integration tests, error handling, alert usability | Beta demo and bug triage |
| 8 | Final data documentation and reproducibility steps | Final model report/model card | Final README, setup, demo and app documentation | Release candidate, presentation and handover |

Isolation Forest is an optional anomaly-detection experiment. Add it after the supervised baseline is reproducible; do not promise it as a required deliverable until the dataset labels and intended use are confirmed.

## 3. Daily/weekly coordination

- Monday: each owner posts 3–5 concrete tasks and expected outputs.
- Wednesday: short blocker check; resolve schema/API changes before code diverges.
- Friday: merge reviewed PRs into `develop`; run integration tests.
- End of week: 5–10 minute demo by each owner and update task status.

Each update must state: completed, next, blocker, PR/commit link.

## 4. Git workflow

- `main`: stable demo/release branch.
- `develop`: integration branch.
- `feature/data-pipeline`, `feature/ai-models`, `feature/dashboard`: individual work branches.
- Create PRs from each feature branch into `develop`.
- Require at least one teammate review and tests before merge.
- Do not force-push shared branches. Rebase/merge latest `develop` into feature branch before PR when needed.
- Only the integration owner merges `develop` into `main` after a release check.

## 5. Definition of done

A task is done only when:
1. Code is committed on the owner's branch.
2. Relevant tests pass locally.
3. Inputs/outputs and assumptions are documented.
4. No secrets, raw AWID3 files, or large unapproved artifacts are committed.
5. A PR is opened with purpose, test evidence, screenshots/metrics where relevant, and known limitations.

## 6. Suggested GitHub issue board columns

`Backlog` → `Ready` → `In Progress` → `Review` → `Done`.

Use labels: `data`, `ai`, `app`, `integration`, `documentation`, `blocked`, `good first task`.

## 7. Important dataset and evaluation rules

- Confirm the exact AWID3 release/files and label field before coding assumptions into the pipeline.
- Keep raw data outside Git; commit only small synthetic fixtures or documented sample metadata.
- Fit preprocessing only on training data; apply the fitted transformer to validation/test data.
- Avoid leakage from duplicate/related records or capture/session grouping. Document the chosen split.
- Report class-wise metrics and macro-F1, not accuracy alone.
- Keep a final untouched test set for the final comparison.
- Clearly distinguish offline AWID3 evaluation from live Wi-Fi monitoring. AWID3 experiments alone do not prove real-time detection capability.
