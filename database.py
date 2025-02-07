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
            INSERT INTO RECORD (telegram_id, type, amount, category, date)
            VALUES (?, ?, ?, ?, ?)
        ''', (telegram_id, record_type, amount, category, date))
        conn.commit()

