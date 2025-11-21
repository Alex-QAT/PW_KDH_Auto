import psycopg2
import pymysql


class DatabaseCleaner:
    def __init__(self, db_type='postgres', **kwargs):
        self.db_type = db_type
        self.connection_params = kwargs

    def clean_tables(self):
        if self.db_type == 'postgres':
            self._clean_postgres()
        elif self.db_type == 'mysql':
            self._clean_mysql()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def _clean_postgres(self):
        try:
            conn = psycopg2.connect(**self.connection_params)
            cursor = conn.cursor()
        #    cursor.execute("DELETE FROM devices;")
            cursor.execute("DELETE FROM status_log_devices;")
            cursor.execute("DELETE FROM devices;")
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ Таблицы status_log_devices и devices в БД PostgreSQL очищены успешно")
        except Exception as e:
            print(f"❌ Ошибка при очистке PostgreSQL: {e}")
            raise

    def _clean_mysql(self):
        try:
            conn = pymysql.connect(**self.connection_params)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM status_log_devices;")
            cursor.execute("DELETE FROM devices;")
            conn.commit()
            cursor.close()
            conn.close()
            print("✅ База данных MySQL очищена успешно")
        except Exception as e:
            print(f"❌ Ошибка при очистке MySQL: {e}")
            raise