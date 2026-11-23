# Wifi-AI Secure

AI-assisted tool for detecting attacks in Wi-Fi networks.

## Project workstreams

| Member | Workstream | Branch |
|---|---|---|
| Hoàng Phúc | AWID3 data ingestion, cleaning, preprocessing, feature engineering | `feature/data-pipeline` |
| Quốc Đạt | ML models, training, evaluation, inference | `feature/ai-models` |
| Tiến Đạt | Backend/API, dashboard, database, alerting | `feature/dashboard` |

## Start here

1. Read [the team work plan](docs/WORK_PLAN.md).
2. Read [the module interface contract](docs/INTERFACE_CONTRACT.md).
3. Clone the repository and check out your assigned branch.
4. Work only in your module's folders and open a pull request to `develop`.

## Important

- AWID3 is research/training data. Do not commit the dataset or large model files to Git.
- Keep raw data local under `data/raw/`; use Git LFS or external storage only if the team explicitly decides to version large artifacts.
- Do not use a random row-level split if it can leak related traffic between train and test. Document the split strategy.
- The initial API/schema examples are contracts for integration, not measured model results.
- Only use this project on networks and traffic captures you are authorized to monitor.

## Proposed stack

- Python 3.11+
- pandas, NumPy, scikit-learn
- XGBoost (optional dependency for the model workstream)
- FastAPI for the backend
- SQLite for the initial local prototype
- Streamlit for the initial dashboard (subject to team agreement)

## Local setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\\Scripts\\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

The application entry points will be added by the respective workstream owners.
