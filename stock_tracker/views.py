# Django
from django.shortcuts import render

# Local files
from .models import Stock, Company
from .forms import StockSearchForm
from .functions import create_company, create_stock

# Custom libraries
import yfinance as yf
import plotly.graph_objs as go


def portfolio(request):
    form = StockSearchForm()
    stock = None
    stock_name = None
    stock_symbol = None
    price = None
    form_error = False
    error_message = None
    if request.method == 'POST':
        form = StockSearchForm(request.POST)

        if form.is_valid():
            stock_ticker = form.cleaned_data['stock_ticker']
            try:
                fetched_stock = yf.Ticker(stock_ticker)
                stock_data = fetched_stock.info

                for info in stock_data:
                    print(info)

                company = create_company(stock_data)
                stock = create_stock(stock_data, company)



            except:
                form_error = True
                error_message = 'Ticker name not valid!'

    context = {
        'form': form,
        'form_error': form_error,
        'error_message': error_message,
        'stock': stock,
    }

    return render(request, 'portfolio/portfolio.html', context)


def plotly_page(request):
    form = StockSearchForm()
    trace = None
    layout = None
    stock_history = []
    graph_type = None
    graph_div = None
    ticker_form = None
    fetched_stock = None

    if request.POST or request.GET:
        form = StockSearchForm(request.POST)
        graph_type = request.GET.get('graph_type',
                                     'line')  # Get the graph type from the query parameter, set default to line
        ticker_form = request.GET.get('stock_ticker')

        if form.is_valid():
            ticker_form = form.cleaned_data['stock_ticker']

        fetched_stock = yf.Ticker(ticker_form)
        history = fetched_stock.history('1mo')
        stock_history = history.reset_index().to_dict('records')  # Convert DataFrame to list of dictionaries

    if fetched_stock is not None:

        if graph_type == 'line':
            dates = [record['Date'].strftime('%Y-%m-%d') for record in stock_history]
            prices = [record['Close'] for record in stock_history]

            trace = go.Scatter(x=dates, y=prices, mode='lines+markers', name='Price')
            layout = go.Layout(title='Historical Price Chart', xaxis=dict(title='Date'), yaxis=dict(title='Price'))

        elif graph_type == 'candlestick':
            trace = go.Candlestick(
                x=[record['Date'] for record in stock_history],
                open=[record['Open'] for record in stock_history],
                high=[record['High'] for record in stock_history],
                low=[record['Low'] for record in stock_history],
                close=[record['Close'] for record in stock_history],
                increasing_line_color='green',  # Customize colors if desired
                decreasing_line_color='red'
            )
            layout = go.Layout(title='Historical Price Chart',
                               xaxis=dict(title='Date'),
                               yaxis=dict(title='Price'))

        graph_div = go.Figure(data=[trace], layout=layout).to_html(full_html=False)

    context = {
        'form': form,
        'stock_ticker': ticker_form,
        'plot_div': graph_div,
        'graph_type': graph_type
    }
    return render(request, 'portfolio/graph.html', context)
