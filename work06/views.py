from django.shortcuts import render
from .forms import ReiwaForm

from django.shortcuts import render

def index(request):
    return render(request, 'work06/index.html')

def reiwa(request):
    result = None
    year_value = None
    if request.method == "POST":
        form = ReiwaForm(request.POST)
        if form.is_valid():
            year_value = form.cleaned_data["year"]
            result = year_value + 2018
    else:
        form = ReiwaForm()

    context = {
        "form": form,
        "result": result,
        "year_value": year_value
    }
    return render(request, "work06/reiwa.html", context)

def bmi(request):
    bmi_value = None
    result = None
    if request.method == "POST":
        height = float(request.POST.get("height", 0))
        weight = float(request.POST.get("weight", 0))
        if height > 0 and weight > 0:
            bmi_value = weight / (height / 100) ** 2
            # 判定
            if bmi_value < 18.5:
                result = "やせ型"
            elif bmi_value < 25:
                result = "普通体重"
            elif bmi_value < 30:
                result = "肥満（1度）"
            else:
                result = "肥満（2度以上）"

    return render(request, "work06/bmi.html", {"bmi": bmi_value, "result": result})

# 💰 貯金計算くん
def savings(request):
    result = None
    if request.method == "POST":
        monthly = int(request.POST.get("monthly", 0))
        months = int(request.POST.get("months", 0))
        if monthly > 0 and months > 0:
            total = monthly * months
            result = f"{months}ヶ月後の貯金総額は {total:,} 円です！"
    return render(request, "work06/savings.html", {"result": result})


# ➕ 四則演算くん
def calc(request):
    result = None
    if request.method == "POST":
        num1 = float(request.POST.get("num1", 0))
        num2 = float(request.POST.get("num2", 0))
        op = request.POST.get("op")

        try:
            if op == "+":
                result = num1 + num2
            elif op == "-":
                result = num1 - num2
            elif op == "*":
                result = num1 * num2
            elif op == "/":
                if num2 != 0:
                    result = round(num1 / num2, 2)
                else:
                    result = "0では割り算できません！"
        except Exception as e:
            result = f"エラー: {e}"

    return render(request, "work06/calc.html", {"result": result})