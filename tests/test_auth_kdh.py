import pytest
from playwright.sync_api import Page, expect


class TestAuthentication:
    """Тесты для аутентификации в системе KDH"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Параметры теста"""
        self.page = page
        self.base_url = "http://192.168.145.148:8080/kdh/login"
        # Тестовые учетные данные
        self.username = "u"
        self.password = "!2345678Aa"

    def fill_login_form(self, username, password):
        """Заполнение формы логина"""
        # Поиск и заполнение поля Login
        self.page.locator('input[name="username"]').fill(username)

        # Поиск и заполнение поля Password
        self.page.locator('input[name="password"]').fill(password)


    def click_sign_in_button(self):
        """Нажатие кнопки Sign In"""
        self.page.locator('button[type="submit"]').click()

    def verify_successful_login(self):
        """Проверка успешной аутентификации по наличию ссылки Logout"""
        logout_link = self.page.get_by_role("link", name="Logout")
        expect(logout_link).to_be_visible()

    def test_successful_login(self):
        """Тест успешной аутентификации пользователя"""
        # Шаг 1: Переход на web-страницу
        self.page.goto(self.base_url)
        expect(self.page).to_have_url(self.base_url)

        # Шаг 2-4: Заполнение формы и вход
        self.fill_login_form(self.username, self.password)
        # self.page.wait_for_timeout(1000)
        self.click_sign_in_button()

        # Ожидание завершения аутентификации
        self.page.wait_for_load_state("networkidle")

        # Шаг 5: Проверка успешной аутентификации
        self.verify_successful_login()




# Параметризованные тесты
@pytest.mark.parametrize("username, password", [
    ("u", "!2345678Aa"),
    ("admin", "!2345678Aa"),
], ids=["regular_user", "admin"])
def test_login_with_parameters(page: Page, username, password):
    """Параметризованный тест логина"""

    page.goto("http://192.168.145.148:8080/kdh/login")

    # Заполнение формы
    page.get_by_placeholder("Login").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Sign In").or_(page.locator('button[type="submit"]')).first.click()

    page.wait_for_load_state("networkidle")

    # Проверка успешного логина
    logout_link = page.get_by_text("Logout")
    expect(logout_link).to_be_visible()


@pytest.mark.parametrize("username, password, expected_success", [
    ("u", "!2345678Aa", True),  # Успешный логин
    ("вася", "!2345678Aa", False),  # Неуспешный логин
], ids=["successful_login", "failed_login"])

def test_login_wright_wrong(page: Page, username, password, expected_success):
    """Параметризованный тест логина с проверкой успешной и неуспешной аутентификации"""

    page.goto("http://192.168.145.148:8080/kdh/login")

    # Заполнение формы
    page.get_by_placeholder("Login").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.wait_for_timeout(1000)
    page.get_by_role("button", name="Sign In").or_(page.locator('button[type="submit"]')).first.click()
    page.wait_for_load_state("networkidle")

    if expected_success:
        # Проверка успешной аутентификации - наличие ссылки Logout
        logout_link = page.get_by_text("Logout")
        expect(logout_link).to_be_visible()
        print("\n\n✅ Успешная аутентификация - ссылка Logout найдена")
    else:
        # Проверка неуспешной аутентификации - наличие сообщения об ошибке
        error_message = page.get_by_text("Invalid username and password!")
        expect(error_message).to_be_visible()
        print("\n\n✅ Неуспешная аутентификация - сообщение об ошибке найдено")

        # Дополнительная проверка - убеждаемся, что ссылки Logout нет
        logout_link = page.get_by_text("Logout")
        expect(logout_link).not_to_be_visible()