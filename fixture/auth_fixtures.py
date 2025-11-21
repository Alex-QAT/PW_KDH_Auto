import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture
def authenticated_page(login_page, credentials):
    """Фикстура для уже авторизованной страницы"""
    login_page.navigate()
    login_page.login(credentials["username"], credentials["password"])
    expect(login_page.page.get_by_text("Logout")).to_be_visible()
    return login_page.page

@pytest.fixture
def admin_authenticated_page(login_page, credentials):
    """Фикстура для авторизации под админом"""
    login_page.navigate()
    login_page.login(credentials["admin_username"], credentials["admin_password"])
    expect(login_page.page.get_by_text("Logout")).to_be_visible()
    return login_page.page