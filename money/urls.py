from django.urls import path
from . import views

app_name = "money"

urlpatterns = [
    path("", views.index, name="index"),
]