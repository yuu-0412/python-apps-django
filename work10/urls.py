from django.urls import path
from . import views

app_name = "work10"

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("create/", views.todo_create, name="todo_create"),
    path("edit/<int:pk>/", views.todo_edit, name="todo_edit"),
    path("delete/<int:pk>/", views.todo_delete, name="todo_delete"),  # ← todo_id → pk に統一
    path("toggle/<int:pk>/", views.toggle_complete, name="toggle_complete"),  # ← ここも pk に
    path("signup/", views.signup, name="signup"),
]