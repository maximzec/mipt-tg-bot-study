import sqlite3
from datetime import datetime

# Имя файла базы данных
DB_NAME = 'budget.db'


def create_tables():
    """Создает таблицы в базе данных, если они не существуют."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS RECORDS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()


def insert_record(telegram_id, record_type, amount, category, date=None):
    """Вставляет запись в таблицу RECORD"""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO RECORDS (telegram_id, type, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, record_type, amount, category, date))
        conn.commit()


def get_unique_categories(telegram_id):
    """Возвращает список уникальных категорий для указанного пользователя."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT category FROM RECORDS
            WHERE telegram_id = ?
        ''', (telegram_id,))
        categories = [row[0] for row in cursor.fetchall()]
    return categories


def get_aggregated_expenses(telegram_id, start_date, end_date, categories=None):
    """Возвращает агрегированную статистику по тратам за указанный период.

    Если указаны категории, возвращает сумму по каждой категории.
    Если категории не указаны, возвращает общую сумму расходов.
    """
    # Добавляем время к датам
    start_date += " 00:00:00"
    end_date += " 23:59:59"

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        if categories:
            # Формируем строку с плейсхолдерами для категорий
            placeholders = ', '.join('?' for _ in categories)
            query = f'''
                SELECT category, SUM(amount) FROM RECORDS
                WHERE telegram_id = ? AND type = 'expense' AND date BETWEEN ? AND ?
                AND category IN ({placeholders})
                GROUP BY category
            '''
            params = (telegram_id, start_date, end_date, *categories)
        else:
            query = '''
                SELECT category, SUM(amount) FROM RECORDS
                WHERE telegram_id = ? AND type = 'expense' AND date BETWEEN ? AND ?
                GROUP BY category
            '''
            params = (telegram_id, start_date, end_date)

        cursor.execute(query, params)

        # Возвращаем сумму по каждой категории
        results = cursor.fetchall()
        return {row[0]: row[1] for row in results}


def get_all_records(telegram_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        query = '''
            SELECT * FROM RECORDS
            WHERE telegram_id = ?
        '''
        cursor.execute(query, (telegram_id,))
        return cursor.fetchall()
