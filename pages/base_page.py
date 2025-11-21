from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url):
        self.page.goto(url)
        self.page.wait_for_load_state("networkidle")

    def wait_for_element_visible(self, selector, timeout=10000):
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def get_element(self, selector):
        return self.page.locator(selector)

    def get_element_by_text(self, text):
        return self.page.get_by_text(text)