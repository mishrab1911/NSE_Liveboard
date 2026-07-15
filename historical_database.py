import sqlite3


class HistoricalDatabase:

    def __init__(self):
        self.db_name = "historical_stocks.db"

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def create_table(self):

        conn = self.get_connection()

        conn.execute("""
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

    def insert_data(self, data):

        conn = self.get_connection()

        conn.execute("""
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

    def get_history(self, symbol):

        conn = self.get_connection()

        rows = conn.execute("""
        SELECT
            stock_datetime,
            current_price
        FROM stock_prices
        WHERE stock_symbol=?
        ORDER BY stock_datetime
        """, (symbol,)).fetchall()

        conn.close()

        return rows