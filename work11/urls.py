# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_data_to_api, name='send_data_to_api'),
]
