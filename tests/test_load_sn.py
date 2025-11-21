import pytest
from playwright.sync_api import expect
from fixture.auth_fixtures import authenticated_page
from pages.devices_page import DevicesPage
from utils.file_helpers import prepare_sn_file, get_sn_test_data
from fixture.database_fixtures import postgres_cleaner, mysql_cleaner
from fixture.auth_fixtures import login_page


def test_import_devices_with_db_cleanup(authenticated_page, postgres_cleaner):
    """Тест импорта устройств с очисткой базы данных при необходимости"""

    # Подготовка данных
    sn_data = get_sn_test_data()
    file_path = prepare_sn_file(
        sn_data["file_dir"],
        sn_data["file_name"],
        sn_data["file_content"]
    )

    # Парсим ожидаемые данные
    expected_data = [line.split('|') for line in sn_data["file_content"].split('\n') if line.strip()]
    expected_serial_numbers = [data[0] for data in expected_data]
    expected_statuses = [data[1] for data in expected_data]

    # Работа со страницей устройств
    devices_page = DevicesPage(authenticated_page)
    devices_page.navigate_to_devices()

    # Проверка предусловия и очистка БД при необходимости
    if devices_page.has_devices():
        print("⚠️ Найдены существующие устройства. Выполняем очистку БД...")
        postgres_cleaner.clean_tables()
        devices_page.page.reload()
        devices_page.page.wait_for_load_state("networkidle")
        assert not devices_page.has_devices(), "Устройства не были удалены из БД"

    # Процесс импорта
    devices_page.open_import_dialog()
    devices_page.click_load_sn_list()
    devices_page.upload_sn_file(file_path)
    devices_page.close_import_modal()

    # Проверка постусловий
    devices_page.page.reload()
    devices_page.page.wait_for_load_state("networkidle")

    # Проверка серийных номеров
    serial_numbers = devices_page.get_serial_numbers()
    actual_count = serial_numbers.count()

    assert actual_count == len(expected_serial_numbers), \
        f"Количество устройств не совпадает: ожидалось {len(expected_serial_numbers)}, получено {actual_count}"

    # Проверка соответствия данных
    actual_serials = [serial_numbers.nth(i).text_content().strip() for i in range(actual_count)]
    actual_statuses = [devices_page.get_device_statuses().nth(i).text_content().strip() for i in range(actual_count)]

    for expected_sn, expected_status in zip(expected_serial_numbers, expected_statuses):
        assert expected_sn in actual_serials, f"Серийный номер {expected_sn} не найден"

    for i, (expected_sn, expected_status) in enumerate(zip(expected_serial_numbers, expected_statuses)):
        if i < len(actual_statuses):
            assert actual_statuses[i] == expected_status, \
                f"Для устройства {expected_sn} ожидался статус '{expected_status}', получен '{actual_statuses[i]}'"

    print("✅ Все проверки пройдены успешно!")