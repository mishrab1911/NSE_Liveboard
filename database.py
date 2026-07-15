import sqlite3
from config import DATABASE_NAME


class DatabaseManager:

    def __init__(self):
        self.db_name = DATABASE_NAME

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_prices(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            stock_symbol TEXT,
            stock_date TEXT,
            stock_time TEXT,
            stock_datetime TEXT,
            min_price REAL,
            max_price REAL,
            current_price REAL
        )
        """)

        conn.commit()
        conn.close()

    def insert_stock_data(self, data):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO stock_prices(
            company_name,
            stock_symbol,
            stock_date,
            stock_time,
            stock_datetime,
            min_price,
            max_price,
            current_price
        )
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            data["company_name"],
            data["stock_symbol"],
            data["stock_date"],
            data["stock_time"],
            data["stock_datetime"],
            data["min_price"],
            data["max_price"],
            data["current_price"]
        ))

        conn.commit()
        conn.close()

    def get_all_data(self):
        conn = self.get_connection()

        data = conn.execute("""
        SELECT *
        FROM stock_prices
        ORDER BY id DESC
        """).fetchall()

        conn.close()

        return data
    
    def get_price_history(self, symbol, minutes):

        conn = self.get_connection()

        query = f"""
        SELECT stock_datetime,current_price
        FROM stock_prices
        WHERE stock_symbol = ?
        AND stock_datetime >= datetime('now','-{minutes} minutes')
        ORDER BY stock_datetime
        """

        data = conn.execute(
            query,
            (symbol,)
        ).fetchall()

        conn.close()

        return data