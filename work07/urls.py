# work07/urls.py
from django.urls import path
from . import views


# work07/urls.py
urlpatterns = [
    path('', views.top, name='top'),
    path('omikuji/', views.omikuji, name='omikuji'),
    path('janken/', views.janken, name='janken'),
    path('hi_low/', views.hi_low, name='hi_low'),
    
]


