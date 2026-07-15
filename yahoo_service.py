import yfinance as yf
from datetime import datetime
from zoneinfo import ZoneInfo


class YahooFinanceService:

    def get_stock_data(self, company_name, symbol):

        stock = yf.Ticker(symbol)

        info = stock.history(period="1d")

        if info.empty:
            return None

        current_price = float(info["Close"].iloc[-1])
        min_price = float(info["Low"].min())
        max_price = float(info["High"].max())

        now = datetime.now(ZoneInfo("Asia/Kolkata"))

        return {
            "company_name": company_name,
            "stock_symbol": symbol,
            "stock_date": now.strftime("%Y-%m-%d"),
            "stock_time": now.strftime("%H:%M:%S"),
            "stock_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "min_price": min_price,
            "max_price": max_price,
            "current_price": current_price
        }
