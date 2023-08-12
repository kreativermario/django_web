from forex_python.converter import CurrencyCodes

from .models import Stock, Company

# Custom libraries
import yfinance as yf


def create_company(stock_data):
    # Company info
    country = stock_data.get('country')
    address = stock_data.get('address1')
    city = stock_data.get('city')
    state = stock_data.get('state')
    website = stock_data.get('website')
    industry = stock_data.get('industry')
    sector = stock_data.get('sector')
    business_summary = stock_data.get('longBusinessSummary')

    company = Company(country=country, address=address, city=city,
                      state=state, website=website, industry=industry,
                      sector=sector, business_summary=business_summary)
    return company


def create_stock(stock_data, company=None):

    # Stock info
    stock_name = stock_data.get('longName')
    stock_symbol = stock_data.get('symbol')

    c = CurrencyCodes()
    currency_code = stock_data.get('currency')
    currency = c.get_symbol(currency_code)

    price = stock_data.get('currentPrice')
    overall_risk = stock_data.get('overallRisk')
    previous_close_price = stock_data.get('previousClose')
    bid_price = stock_data.get('bid')
    ask_price = stock_data.get('ask')
    open_price = stock_data.get('open')

    exchange = stock_data.get('exchange')

    if company is None:
        #TODO Raise custom exception

    stock = Stock(name=stock_name,
                  symbol=stock_symbol,
                  price=price,
                  currency=currency,
                  exchange=exchange,
                  company=company,
                  overall_risk=overall_risk,
                  previous_close_price=previous_close_price,
                  bid_price=bid_price,
                  ask_price=ask_price,
                  open_price=open_price)
    return stock