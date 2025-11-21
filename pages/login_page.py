from playwright.sync_api import expect
from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "http://192.168.145.148:8080/kdh/login"

    def navigate(self):
        self.navigate_to(self.url)
        expect(self.page).to_have_url(self.url)

    def fill_login_form(self, username: str, password: str):
        """Заполнение формы логина"""
        self.page.locator('input[name="username"]').fill(username)
        self.page.locator('input[name="password"]').fill(password)

    def click_sign_in(self):
        """Нажатие кнопки Sign In"""
        self.page.locator('button[type="submit"]').click()
        self.page.wait_for_load_state("networkidle")

    def login(self, username: str, password: str):
        """Полный процесс логина"""
        self.fill_login_form(username, password)
        self.click_sign_in()

    def is_logged_in(self) -> bool:
        """Проверка успешного логина"""
        try:
            expect(self.page.get_by_text("Logout")).to_be_visible(timeout=5000)
            return True
        except:
            return False

    def get_error_message(self):
        """Получение сообщения об ошибке"""
        return self.page.get_by_text("Invalid username and password!")