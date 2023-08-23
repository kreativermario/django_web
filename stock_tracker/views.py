# Django
from django.shortcuts import render

# Local files
from .models import Stock, Company
from .forms import StockSearchForm
from .functions import create_company, create_stock, create_line_graph, \
    create_area_graph, create_candlestick_graph

# Custom libraries
import yfinance as yf
import plotly.graph_objs as go


def home_view(request):
    return render(request, 'stocks/home.html', {})


def stock_info(request):
    form = StockSearchForm()
    stock = None
    form_error = False
    fix_error_message = None
    error_message = None
    if request.method == 'POST':
        form = StockSearchForm(request.POST)

        if form.is_valid():
            stock_ticker = form.cleaned_data['stock_ticker']
            try:
                fetched_stock = yf.Ticker(stock_ticker)
                stock_data = fetched_stock.info

                company = create_company(stock_data)
                stock = create_stock(stock_data, company)
            except:
                form_error = True
                error_message = 'Ticker name not valid!'
                fix_error_message = 'Maybe try searching for a valid stock ticker?'
    context = {
        'form': form,
        'form_error': form_error,
        'error_message': error_message,
        'fix_error_message': fix_error_message,
        'stock': stock,
    }

    return render(request, 'stocks/stock_info.html', context)


def stock_history(request):
    form = StockSearchForm()
    trace = None
    layout = None
    timeline = None
    historic_data = []
    graph_type = None
    graph_div = None
    ticker_form = None
    fetched_stock = None
    stock_name = None
    form_error = False
    fix_error_message = None
    error_message = None

    if request.POST or request.GET:
        form = StockSearchForm(request.POST)
        graph_type = request.GET.get('graph_type',
                                     'line')  # Get the graph type from the query parameter, set default to line
        ticker_form = request.GET.get('stock_ticker')
        timeline = request.GET.get('timeline', 'ytd')

        try:
            if form.is_valid():
                ticker_form = form.cleaned_data['stock_ticker']

            fetched_stock = yf.Ticker(ticker_form)
            stock_name = fetched_stock.info.get('longName')
            history = fetched_stock.history(timeline)
            historic_data = history.reset_index().to_dict('records')  # Convert DataFrame to list of dictionaries
        except:
            form_error = True
            error_message = 'Ticker name not valid!'
            fix_error_message = 'Maybe try searching for a valid stock ticker? ' \
                                'If you\'re trying to search for an ETF like VWCE, try VWCE.de. ' \
                                'The de is the stock market. For example: IWDA.as (Euronext Amsterdam)'

    if fetched_stock is not None:

        if graph_type == 'line':
            trace, layout = create_line_graph(historic_data)

        elif graph_type == 'area':
            trace, layout = create_area_graph(historic_data)

        elif graph_type == 'candlestick':
            trace, layout = create_candlestick_graph(historic_data)

        graph_div = go.Figure(data=[trace], layout=layout).to_html(full_html=False)

    context = {
        'form': form,
        'stock_name': stock_name,
        'stock_ticker': ticker_form,
        'graph_type': graph_type,
        'timeline': timeline,
        'plot_div': graph_div,
        'form_error': form_error,
        'error_message': error_message,
        'fix_error_message': fix_error_message,
    }
    return render(request, 'stocks/graph.html', context)
