from .models import Stock, Company

# Custom libraries
import yfinance as yf
import plotly.graph_objs as go
from forex_python.converter import CurrencyCodes


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

    # TODO if company is None throw exception

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


def create_line_graph(historic_data):
    dates = [record['Date'].strftime('%Y-%m-%d') for record in historic_data]
    prices = [record['Close'] for record in historic_data]

    trace = go.Scatter(x=dates, y=prices,
                       mode='lines+markers',
                       name='Price',
                       line=dict(color='green'))
    layout = go.Layout(title='Historical Price Chart',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Price'))

    return trace, layout


def create_area_graph(historic_data):
    dates = [record['Date'].strftime('%Y-%m-%d') for record in historic_data]
    prices = [record['Close'] for record in historic_data]

    trace = go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        fill='tozeroy',
        line=dict(color='green'),  # Set the line color
        fillcolor='rgba(93, 187, 99, 1)'  # Set the fill color with transparency
    )
    layout = go.Layout(title='Historical Price Chart',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Price'))

    return trace, layout


def create_candlestick_graph(historic_data):
    trace = go.Candlestick(
        x=[record['Date'] for record in historic_data],
        open=[record['Open'] for record in historic_data],
        high=[record['High'] for record in historic_data],
        low=[record['Low'] for record in historic_data],
        close=[record['Close'] for record in historic_data],
        increasing_line_color='green',  # Customize colors if desired
        decreasing_line_color='red'
    )
    layout = go.Layout(title='Stock Historical Price Chart',
                       xaxis=dict(title='Date'),
                       yaxis=dict(title='Price'))

    return trace, layout