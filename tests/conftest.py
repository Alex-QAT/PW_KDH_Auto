import pytest
from playwright.sync_api import Playwright, Browser

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright: Playwright):
    """Конфигурация контекста браузера"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
        "ignore_https_errors": True,
    }
