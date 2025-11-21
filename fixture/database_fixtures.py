import pytest
from utils.database import DatabaseCleaner

@pytest.fixture
def database_cleaner():
    """Фикстура для очистки БД"""
    def _cleaner(db_type='postgres', **kwargs):
        return DatabaseCleaner(db_type=db_type, **kwargs)
    return _cleaner

@pytest.fixture
def postgres_cleaner(database_cleaner):
    """Фикстура для очистки PostgreSQL"""
    return database_cleaner(
        db_type='postgres',
        host='192.168.145.148',
        database='kdh_tink_autoqa',
        user='postgres',
        password='123456',
        port=5432
    )

@pytest.fixture
def mysql_cleaner(database_cleaner):
    """Фикстура для очистки MySQL"""
    return database_cleaner(
        db_type='mysql',
        host='localhost',
        database='kdh_database',
        user='your_username',
        password='your_password',
        port=3306,
        charset='utf8mb4'
    )