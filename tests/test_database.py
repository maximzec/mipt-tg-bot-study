import unittest
import sqlite3
from datetime import datetime
from database import create_tables, insert_record, get_unique_categories, get_aggregated_expenses, get_all_records


class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        # Устанавливаем базу данных в памяти
        self.db_name = 'memory.db'
        create_tables(self.db_name)
        # Проверка, что таблица records существует
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='RECORDS';")
            assert cursor.fetchone() is not None, "Таблица records не была создана"

    def tearDown(self):
        # Закрываем соединение после каждого теста
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM RECORDS")
            conn.commit()

    def clear_tables(self):
        # Очистка всех таблиц
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM RECORDS")
            conn.commit()

    def test_insert_record_and_get_all_records(self):
        insert_record(self.db_name, 12345, 'income', 1000, 'salary')
        records = get_all_records(self.db_name, 12345)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][2], 'income')
        self.assertEqual(records[0][3], 1000)
        self.assertEqual(records[0][4], 'salary')

    def test_get_unique_categories(self):
        insert_record(self.db_name, 12345, 'income', 1000, 'salary')
        insert_record(self.db_name, 12345, 'expense', 200, 'food')
        insert_record(self.db_name, 12345, 'expense', 300, 'transport')
        categories = get_unique_categories(self.db_name, 12345)
        self.assertEqual(set(categories), {'salary', 'food', 'transport'})

    def test_get_aggregated_expenses(self):
        insert_record(self.db_name, 12345, 'expense',
                      200, 'food', '2023-10-01 10:00:00')
        insert_record(self.db_name, 12345, 'expense', 300,
                      'transport', '2023-10-02 12:00:00')
        insert_record(self.db_name, 12345, 'expense',
                      100, 'food', '2023-10-03 14:00:00')
        start_date = '2023-10-01'
        end_date = '2023-10-03'
        expenses = get_aggregated_expenses(
            self.db_name, 12345, start_date, end_date)
        self.assertEqual(expenses['food'], 300)
        self.assertEqual(expenses['transport'], 300)

    def test_get_aggregated_expenses_with_categories(self):
        insert_record(self.db_name, 12345, 'expense',
                      200, 'food', '2023-10-01 10:00:00')
        insert_record(self.db_name, 12345, 'expense', 300,
                      'transport', '2023-10-02 12:00:00')
        insert_record(self.db_name, 12345, 'expense',
                      100, 'food', '2023-10-03 14:00:00')
        start_date = '2023-10-01'
        end_date = '2023-10-03'
        expenses = get_aggregated_expenses(
            self.db_name, 12345, start_date, end_date, ['food'])
        self.assertEqual(expenses['food'], 300)
        self.assertNotIn('transport', expenses)


if __name__ == '__main__':
    unittest.main()
