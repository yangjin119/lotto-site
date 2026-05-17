# lotto/urls.py
from django.urls import path
from . import views

app_name = 'lotto'

urlpatterns = [
    path('buy/', views.buy_lotto, name='buy_lotto'),
]