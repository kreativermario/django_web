from django.urls import path
from . import views

app_name = 'stock_tracker'
urlpatterns = [
    path('', views.home_view, name='home'),
    path('info/', views.stock_info, name='stock_info'),
    path('history/', views.stock_history, name='stock_history'),
    # Define other URL patterns here
]
