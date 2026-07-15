from config import COMPANIES
from yahoo_service import YahooFinanceService
from database import DatabaseManager


class StockService:

    def __init__(self):
        self.yahoo_service = YahooFinanceService()
        self.database = DatabaseManager()

    def load_stock_data(self):

        for company_name, symbol in COMPANIES.items():

            stock_data = self.yahoo_service.get_stock_data(
                company_name,
                symbol
            )

            if stock_data:
                self.database.insert_stock_data(stock_data)