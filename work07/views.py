from django.shortcuts import render
import random

def top(request):
    return render(request, 'work07/top.html')

def omikuji(request):
    results = ['大吉', '中吉', '小吉', '吉', '末吉', '凶']
    result = None

    if request.method == 'POST':  # ボタンを押したとき
        result = random.choice(results)
    return render(request, 'work07/omikuji.html', {'result': result})

def janken(request):
    choices = ["グー", "チョキ", "パー"]
    result = ""
    user_hand = ""
    computer_hand = ""  # ← GET時も空で定義しておく

    if request.method == "POST":
        user_hand = request.POST.get("hand")
        computer_hand = random.choice(choices)

        if user_hand == computer_hand:
            result = "あいこ！"
        elif (user_hand == "グー" and computer_hand == "チョキ") or \
             (user_hand == "チョキ" and computer_hand == "パー") or \
             (user_hand == "パー" and computer_hand == "グー"):
            result = "あなたの勝ち！"
        else:
            result = "あなたの負け！"

    # 👇 これが重要：POSTでもGETでも最終的にrenderする！
    return render(request, "work07/janken.html", {
        "user_hand": user_hand,
        "computer_hand": computer_hand,
        "result": result
    })
    
def hi_low(request):
    result = ""
    user_number = ""

    # 初期化
    if "computer_number" not in request.session:
        request.session["computer_number"] = random.randint(1, 100)
        request.session["attempts"] = 0

    computer_number = request.session["computer_number"]
    attempts = request.session["attempts"]

    if request.method == "POST":
        user_number = request.POST.get("number")
        if user_number:
            user_number = int(user_number)
            attempts += 1
            request.session["attempts"] = attempts

            if user_number > computer_number:
                result = "Low！"
            elif user_number < computer_number:
                result = "Hi！"
            else:
                result = f"ピッタリ一致！あなたの数字は {user_number} です！"
                del request.session["computer_number"]
                del request.session["attempts"]

            # 5回目で当たらなかった場合、答えを表示
            if attempts >= 5 and user_number != computer_number:
                result = f"5回挑戦しました！答えは {computer_number} でした。"
                del request.session["computer_number"]
                del request.session["attempts"]

    return render(request, "work07/hi_low.html", {
        "result": result,
        "user_number": user_number,
        "attempts": attempts
    })