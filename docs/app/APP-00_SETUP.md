
# APP-00 - Application Project Skeleton

## 1. Project Information

- Project: Wifi-AI Secure
- Task: APP-00
- Wave: 0.1
- Owner: Tiến Đạt
- Branch: feature/dashboard
- Python: 3.11.9
- Development OS: Windows

## 2. Objectives

- Initialize the Application project structure.
- Build the FastAPI backend skeleton.
- Build the Streamlit dashboard skeleton.
- Configure the development environment.
- Implement automated smoke tests.

## 3. Project Structure

    src/
        alerts/
            __init__.py
        api/
            __init__.py
            main.py
        app/
            __init__.py
            main.py
            README.md
        database/
            __init__.py
    tests/
        api/
            test_health.py
        app/
            test_dashboard.py
    requirements-app.txt
    .gitignore

## 4. Environment Setup

Run the following commands from the repository root:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements-app.txt
python -m pip check
```

## 5. Run Backend

```powershell
python -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8000
```

Available endpoints:

- GET / : Application information
- GET /health : Service health check
- GET /docs : Swagger UI
- GET /openapi.json : OpenAPI schema

Backend URL: http://127.0.0.1:8000

## 6. Run Dashboard

Open another terminal and activate the virtual environment.

```powershell
.\.venv\Scripts\Activate.ps1
python -m streamlit run src/app/main.py --server.address 127.0.0.1 --server.port 8501
```

Dashboard URL: http://127.0.0.1:8501

Available pages:

- Tổng quan
- AI Detection
- Model Evaluation
- Attack History

## 7. Automated Testing

```powershell
python -m pytest tests/api tests/app -v
```

### Test Results

- Test date: 2026-11-24
- Python: 3.11.9
- Backend tests: 4/4 PASSED
- Dashboard tests: 2/2 PASSED
- Total tests: 6
- Passed: 6
- Failed: 0
- Warnings: 1
- Pass rate: 100%
- Execution time: 1.22 seconds

### Test Cases

| Test case | Result |
|---|---|
| test_root | PASS |
| test_health_check | PASS |
| test_unknown_endpoint | PASS |
| test_openapi_schema | PASS |
| test_dashboard_startup | PASS |
| test_dashboard_navigation | PASS |

## 8. Known Issues

- StarletteDeprecationWarning related to httpx.
- The warning does not cause test failures.
- Dependency compatibility will be reviewed by the team.

## 9. Current Limitations

- AWID3 dataset is not integrated.
- AI models are not integrated.
- SQLite persistence is not implemented.
- Alert Engine is not implemented.
- Dashboard and Backend run independently.

These features will be implemented in subsequent waves.

## 10. Acceptance Status

- Application skeleton: Completed.
- Backend smoke tests: Passed.
- Dashboard smoke tests: Passed.
- Combined tests: Passed.
- Pull Request: Pending.
- Team review: Pending.
