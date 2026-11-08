
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

from work10 import views as work10_views


urlpatterns = [
    # ルートURLはTODO一覧にリダイレクト
    path("", lambda request: redirect("work10:todo_list"), name="home"),

    path("admin/", admin.site.urls),

    # 時計アプリ
    path("clock/", include("clock.urls")),

    # その他のアプリ
    path("work05/", include("work05.urls")),
    path("work06/", include("work06.urls")),
    path("work07/", include("work07.urls")),
    path("work08/", include("work08.urls")),
    path("work09/", include("work09.urls")),
    path("work10/", include("work10.urls")),
    path("work11/", include("work11.urls")),

    # 認証関連
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="work10/login.html"
        ),
        name="login"
    ),

    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page=settings.LOGIN_URL
        ),
        name="logout"
    ),

    path(
        "signup/",
        work10_views.signup,
        name="signup"
    ),
]
