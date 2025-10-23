"""
URL configuration for python_apps_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from work10 import views as work10_views

urlpatterns = [
    # ルートURLはTODO一覧にリダイレクト
    path("", lambda request: redirect("work10:todo_list"), name="home"),

    path("admin/", admin.site.urls),
    path("work05/", include("work05.urls")),
    path("work06/", include("work06.urls")),
    path("work07/", include("work07.urls")),
    path("work08/", include("work08.urls")),
    path("work09/", include("work09.urls")),
    path("work10/", include("work10.urls")),

    # 認証関連
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="work10/login.html"),
        name="login"
    ),
    path('logout/', auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL), name='logout'),
    
    path(
        "signup/",
        work10_views.signup,
        name="signup"
    ),
]

# 開発環境でのメディアファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)