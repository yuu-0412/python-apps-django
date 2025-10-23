from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.memo_list, name='memo_list'),
    path('create/', views.memo_create, name='memo_create'),
    path('edit/<int:memo_id>/', views.memo_edit, name='memo_edit'),
    path('delete/<int:memo_id>/', views.memo_delete, name='memo_delete'),
]

# 開発中のみメディアファイルを表示できるように追加
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)