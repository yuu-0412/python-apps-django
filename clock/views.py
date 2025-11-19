from django.shortcuts import render
from datetime import datetime

def index(request):
    now = datetime.now().hour
    if 5 <= now < 11:
        message = "おはよう☀️ 今日もいい朝だね！"
    elif 11 <= now < 17:
        message = "こんにちは🌼 無理せずいこう！"
    elif 17 <= now < 22:
        message = "こんばんは🌙 おつかれさま！"
    else:
        message = "そろそろおやすみ💤"
    return render(request, 'tokei/index.html', {'message': message})