from django.urls import path
from . import views

app_name = 'aviation_app'
urlpatterns = [
    path('', views.flight_list, name='flight_list'),
    # Define other URL patterns here
]
