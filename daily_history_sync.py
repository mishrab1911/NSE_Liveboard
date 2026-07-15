# Every day at 3:32 PM
# Take latest row from stocks.db
# Insert into historical_stocks.db


import time
import sqlite3
from datetime import datetime


while True:

    now = datetime.now()

    if now.hour == 15 and now.minute == 32:

        live_conn = sqlite3.connect("stocks.db")

        row = live_conn.execute("""
        SELECT
            company_name,
            stock_symbol,
            stock_date,
            stock_time,
            stock_datetime,
            min_price,
            max_price,
            current_price
        FROM stock_prices
        ORDER BY id DESC
        LIMIT 1
        """).fetchone()

        live_conn.close()

        if row:

            hist_conn = sqlite3.connect(
                "historical_stocks.db"
            )

            hist_conn.execute("""
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
            """, row)

            hist_conn.commit()
            hist_conn.close()

            print("Historical DB Updated")

        time.sleep(60)

    time.sleep(10)