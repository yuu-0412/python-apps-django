
import uuid
import re
import mimetypes

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import Http404, FileResponse

from .models import ClockPhoto, ClockSetting
from .forms import ClockPhotoForm


def is_valid_owner_id(owner_id):
    return bool(owner_id and re.fullmatch(r"[0-9a-f]{32}", owner_id))


def get_owner_id(request):
    owner_id = request.COOKIES.get("clock_owner_id")

    if not is_valid_owner_id(owner_id):
        owner_id = uuid.uuid4().hex

    return owner_id


def get_clock_setting(owner_id):
    setting, created = ClockSetting.objects.get_or_create(
        owner_id=owner_id
    )
    return setting


def set_owner_cookie(response, owner_id):
    response.set_cookie(
        "clock_owner_id",
        owner_id,
        max_age=60 * 60 * 24 * 365,
        httponly=True,
        samesite="Lax",
        secure=not settings.DEBUG,
        path="/clock/",
    )
    return response


# 時計画面
def index(request):
    owner_id = get_owner_id(request)
    setting = get_clock_setting(owner_id)

    now = timezone.localtime()
    hour = now.hour

    if 5 <= hour < 11:
        message = "おはよう☀️ 今日もいい朝だね！"
    elif 11 <= hour < 17:
        message = "こんにちは🌼 無理せずいこう！"
    elif 17 <= hour < 22:
        message = "こんばんは🌙 おつかれさま！"
    else:
        message = "そろそろおやすみ💤"

    response = render(request, "clock/index.html", {
        "message": message,
        "photo": setting.selected_photo,
        "range_60": range(0, 61),
    })

    return set_owner_cookie(response, owner_id)


# 壁紙設定画面
def settings_view(request):
    owner_id = get_owner_id(request)
    setting = get_clock_setting(owner_id)
    form = ClockPhotoForm()

    if request.method == "POST":

        # 写真アップロード
        if request.POST.get("action") == "upload":
            form = ClockPhotoForm(request.POST, request.FILES)

            if form.is_valid():
                photo = form.save(commit=False)
                photo.owner_id = owner_id
                photo.save()

                response = redirect("clock:settings")
                return set_owner_cookie(response, owner_id)

        # 背景選択
        elif request.POST.get("action") == "select":
            photo_id = request.POST.get("selected_photo")

            if photo_id:
                photo = get_object_or_404(
                    ClockPhoto,
                    id=photo_id,
                    owner_id=owner_id
                )

                setting.selected_photo = photo
                setting.save()

                response = redirect("clock:settings")
                return set_owner_cookie(response, owner_id)

        # 写真削除
        elif request.POST.get("action") == "delete":
            photo_id = request.POST.get("photo_id")

            if photo_id:
                photo = get_object_or_404(
                    ClockPhoto,
                    id=photo_id,
                    owner_id=owner_id
                )

                # 現在の背景なら設定を解除
                if setting.selected_photo_id == photo.id:
                    setting.selected_photo = None
                    setting.save()

                # 画像ファイルを削除
                if photo.image:
                    photo.image.delete(save=False)

                # データベースから削除
                photo.delete()

                response = redirect("clock:settings")
                return set_owner_cookie(response, owner_id)

    photos = ClockPhoto.objects.filter(
        owner_id=owner_id
    ).order_by("-uploaded_at")

    response = render(request, "clock/settings.html", {
        "form": form,
        "photos": photos,
        "setting": setting,
    })

    return set_owner_cookie(response, owner_id)


# 写真を背景に設定
@require_POST
def set_bg(request, photo_id):
    owner_id = get_owner_id(request)
    setting = get_clock_setting(owner_id)

    photo = get_object_or_404(
        ClockPhoto,
        id=photo_id,
        owner_id=owner_id
    )

    setting.selected_photo = photo
    setting.save()

    response = redirect("clock:settings")
    return set_owner_cookie(response, owner_id)


# 保存した写真を表示
def serve_photo(request, photo_id):
    owner_id = request.COOKIES.get("clock_owner_id")

    if not is_valid_owner_id(owner_id):
        raise Http404

    photo = get_object_or_404(
        ClockPhoto,
        id=photo_id,
        owner_id=owner_id
    )

    try:
        image_file = photo.image.open("rb")

        content_type = (
            mimetypes.guess_type(photo.image.name)[0]
            or "application/octet-stream"
        )

        return FileResponse(
            image_file,
            content_type=content_type
        )

    except (FileNotFoundError, OSError, ValueError):
        raise Http404
