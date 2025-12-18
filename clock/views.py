from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import ClockPhoto, ClockSetting
from .forms import ClockPhotoForm  # 後でフォーム作成します

def index(request):
    """時計画面"""
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

    # 設定画面で選ばれた背景
    setting = ClockSetting.objects.first()
    selected_photo = setting.selected_photo if setting else None

    return render(request, "clock/index.html", {
        "message": message,
        "photo": selected_photo,
        "range_60": range(0, 61),
    })


def settings_view(request):
    """設定画面"""
    photos = ClockPhoto.objects.all()
    setting, created = ClockSetting.objects.get_or_create(id=1)

    if request.method == "POST":
        # 写真アップロード
        form = ClockPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("clock:settings")

        # 背景写真を選択
        selected_id = request.POST.get("selected_photo")
        if selected_id:
            setting.selected_photo_id = selected_id
            setting.save()
            return redirect("clock:settings")
    else:
        form = ClockPhotoForm()

    return render(request, "clock/settings.html", {
        "photos": photos,
        "setting": setting,
        "form": form,
    })


def set_bg(request, photo_id):
    """特定の写真を背景に設定"""
    setting, created = ClockSetting.objects.get_or_create(id=1)
    photo = get_object_or_404(ClockPhoto, id=photo_id)
    setting.selected_photo = photo
    setting.save()
    return redirect("clock:settings")


def upload_photo(request):
    """写真アップロード用のビュー（POST専用）"""
    if request.method == "POST" and "image" in request.FILES:
        ClockPhoto.objects.create(image=request.FILES["image"])
    return redirect("clock:settings")