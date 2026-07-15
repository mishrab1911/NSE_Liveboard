import time

from stock_service import StockService
from database import DatabaseManager

db = DatabaseManager()
db.create_table()

service = StockService()

print("Running Data Collector...")

while True:

    try:
        service.load_stock_data()
        print("Data Updated")
    except Exception as e:
        print(e)

    time.sleep(3)