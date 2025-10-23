from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='work06_index'),           # ← 追加（トップページを直接表示）
    path('index/', views.index, name='work06_index'),
    path('reiwa/', views.reiwa, name='work06_reiwa'),
     path('bmi/', views.bmi, name='work06_bmi'),
    path('savings/', views.savings, name='work06_savings'),
    path('calc/', views.calc, name='work06_calc'),
]
