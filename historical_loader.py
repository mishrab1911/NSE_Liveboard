
# Download 10 years data from Yahoo
# Store into historical_stocks.db

import yfinance as yf

from config import COMPANIES
from historical_database import HistoricalDatabase

db = HistoricalDatabase()

db.create_table()

for company, symbol in COMPANIES.items():

    print(f"Loading {company}")

    data = yf.download(
        symbol,
        period="10y",
        interval="1d",
        progress=False,
        auto_adjust=False
    )

    if data.empty:
        print(f"No data found for {symbol}")
        continue

    for index, row in data.iterrows():

        record = {

            "company_name": company,
            "stock_symbol": symbol,

            "stock_date": str(index.date()),

            "stock_time": "15:30:00",

            "stock_datetime": f"{index.date()} 15:30:00",

            "min_price": float(row["Low"].item()),
            "max_price": float(row["High"].item()),
            "current_price": float(row["Close"].item())

        }

        db.insert_data(record)

    print(f"{company} completed")

print("10 Years History Loaded Successfully")