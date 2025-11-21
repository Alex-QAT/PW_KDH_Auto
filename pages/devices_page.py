from playwright.sync_api import expect
from .base_page import BasePage


class DevicesPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def navigate_to_devices(self):
        """Переход на страницу Devices"""
        self.page.get_by_text("Devices", exact=True).click()
        self.page.wait_for_load_state("networkidle")

    def get_device_rows(self):
        """Получение строк с устройствами"""
        return self.page.locator("body > div.container.ng-scope > div:nth-child(4) > div > table > tbody > tr")

    def has_devices(self) -> bool:
        """Проверка наличия устройств"""
        return self.get_device_rows().count() > 0

    def open_import_dialog(self):
        """Открытие диалога импорта"""
        import_icon = self.page.locator('span.glyphicon.glyphicon-import')
        expect(import_icon).to_be_visible(timeout=10000)
        import_icon.click()

    def click_load_sn_list(self):
        """Клик по ссылке Load S/N list"""
        load_sn_link = self.page.get_by_text("Load S/N list", exact=True)
        expect(load_sn_link).to_be_visible(timeout=10000)
        load_sn_link.click()

    def upload_sn_file(self, file_path: str):
        """Загрузка файла с серийными номерами"""
        file_input = self.page.locator('#deviceFile')
    #    expect(file_input).to_be_visible(timeout=5000)
        file_input.set_input_files(file_path)
        self.page.wait_for_timeout(2000)

    def close_import_modal(self):
        """Закрытие модального окна импорта"""
        close_button = self.page.locator('button.btn.btn-primary[ng-click="ok()"]')
        expect(close_button).to_be_visible(timeout=10000)
        expect(close_button).not_to_be_disabled(timeout=15000)
        close_button.click()
        expect(close_button).not_to_be_visible(timeout=10000)

    def get_serial_numbers(self):
        """Получение списка серийных номеров"""
        return self.page.locator(
            'td[ng-if="devicesCtrl.fields[devicesCtrl.fieldIndex + 0].show"][ng-bind="device.serialNumber"]')

    def get_device_statuses(self):
        """Получение списка статусов устройств"""
        return self.page.locator('span[ng-bind="device.status.original.title"][ng-if="!device.status.editing"]')