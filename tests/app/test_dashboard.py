
from pathlib import Path

from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "src" / "app" / "main.py"


def test_dashboard_startup():
    app = AppTest.from_file(
        str(APP_PATH),
        default_timeout=10,
    )
    app.run()

    assert not app.exception
    assert app.title[0].value == "Tổng quan"


def test_dashboard_navigation():
    app = AppTest.from_file(
        str(APP_PATH),
        default_timeout=10,
    )
    app.run()

    pages = [
        "Tổng quan",
        "AI Detection",
        "Model Evaluation",
        "Attack History",
    ]

    for page in pages:
        app.sidebar.radio[0].set_value(page).run()

        assert not app.exception
        assert app.title[0].value == page
