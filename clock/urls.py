
from django.urls import path
from . import views

app_name = "clock"

urlpatterns = [
    path("", views.index, name="index"),

    path("settings/", views.settings_view, name="settings"),

    path(
        "set-bg/<int:photo_id>/",
        views.set_bg,
        name="set_bg"
    ),

    path(
        "photo/<int:photo_id>/",
        views.serve_photo,
        name="serve_photo"
    ),
]
