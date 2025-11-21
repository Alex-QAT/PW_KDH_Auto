import pytest
from playwright.sync_api import expect
from fixture.auth_fixtures import login_page
from pages.login_page import LoginPage


#class TestAuthentication:
#    """Тесты для аутентификации в системе KDH"""

#    def test_successful_login(self, login_page: LoginPage, credentials):
#        """Тест успешной аутентификации пользователя"""
#        login_page.navigate()
#        login_page.login(credentials["username"], credentials["password"])
#        assert login_page.is_logged_in()


#@pytest.mark.parametrize("username, password", [
#    ("u", "!2345678Aa"),
#    ("admin", "!2345678Aa"),
#], ids=["regular_user", "admin"])
#def test_login_with_parameters(login_page: LoginPage, username, password):
#    """Параметризованный тест логина"""
#    login_page.navigate()
#    login_page.login(username, password)
#    assert login_page.is_logged_in()


@pytest.mark.parametrize("username, password, expected_success", [
    ("u", "!2345678Aa", True),
    ("вася", "!2345678Aa", False),
], ids=["successful_login", "failed_login"])
def test_login_right_wrong(login_page: LoginPage, username, password, expected_success):
    """Параметризованный тест с проверкой успешной и неуспешной аутентификации"""
    login_page.navigate()
    login_page.login(username, password)

    if expected_success:
        assert login_page.is_logged_in()
        print("\n\n✅ Успешная аутентификация - ссылка Logout найдена")
    else:
        expect(login_page.get_error_message()).to_be_visible()
        assert not login_page.is_logged_in()
        print("\n\n✅ Неуспешная аутентификация - сообщение об ошибке найдено")