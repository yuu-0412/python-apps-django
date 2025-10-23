from django.urls import path
from . import views

app_name = "work09"

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("create/", views.todo_create, name="todo_create"),
    path("edit/<int:pk>/", views.todo_edit, name="todo_edit"),
    path("delete/<int:todo_id>/", views.todo_delete, name="todo_delete"),
    path('toggle/<int:todo_id>/', views.toggle_complete, name='toggle_complete'),
]

