from django.urls import path
from . import views

app_name = 'stock_tracker'
urlpatterns = [
    path('', views.portfolio, name='portfolio_view'),
    path('plotly-page/', views.plotly_page, name='plotly_page'),
    # Define other URL patterns here
]
