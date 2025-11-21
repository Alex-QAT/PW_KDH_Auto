import pytest
from playwright.sync_api import Playwright, Page

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright: Playwright):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }

@pytest.fixture(scope="session")
def base_url():
    return "http://192.168.145.148:8080/kdh"

@pytest.fixture
def credentials():
    return {
        "username": "u",
        "password": "!2345678Aa",
        "admin_username": "admin",
        "admin_password": "!2345678Aa"
    }

pytest_plugins = [
    "fixture.database_fixtures",
    # другие ваши фикстуры...
]