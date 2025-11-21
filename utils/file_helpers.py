import os
from pathlib import Path


def prepare_sn_file(file_dir: str, file_name: str, content: str) -> str:
    """Подготовка файла для импорта"""
    Path(file_dir).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(file_dir, file_name)

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Файл создан: {file_path}")
    else:
        print(f"✅ Файл уже существует: {file_path}")

    assert os.path.exists(file_path), f"Файл {file_path} не найден"
    return file_path


def get_sn_test_data():
    """Тестовые данные для импорта"""
    return {
        "file_content": """0910022977|NEW
2331753516|NEW
2760015174|NEW
5C038839|NEW
11111111|NEW
2222222222|NEW
401518439|NEW
331641587|NEW
2820053354|NEW""",
        "file_dir": r"d:\AutoQA_files_upload\SN_files\TINKOFF",
        "file_name": "DTS_KDH_20231129_0010_TEST_SN_LIST.TXT"
    }