import sqlite3
from datetime import date

def create_table():
    conn = sqlite3.connect("agendamentos.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pet_name TEXT,
        date TEXT,
        service TEXT,
        weight_or_size TEXT
    )
    """)
    conn.commit()
    conn.close()

def inserir_agendamento(pet_name: str, data: date, service: str, size: str):
    conn = sqlite3.connect("agendamentos.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO agendamentos (pet_name, date, service, weight_or_size)
    VALUES (?, ?, ?, ?)
    """, (pet_name, data.isoformat(), service, size))
    conn.commit()
    conn.close()