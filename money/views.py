from django.shortcuts import render
from .models import MonthlyBudget, Expense, TreeStatus
from django.db.models import Sum
from datetime import date

def index(request):
    # 今月の予算
    budget = MonthlyBudget.objects.last()
    total = Expense.objects.aggregate(total=Sum("price"))["total"] or 0
    remaining = budget.amount - total if budget else 0

    # 今日の支出
    today_spent = Expense.objects.filter(
        created_at__date=date.today()
    ).aggregate(total=Sum("price"))["total"] or 0

    # 金のなる木の状態を取得（なければ作る）
    tree, created = TreeStatus.objects.get_or_create(id=1)

    message = None

    if request.method == "POST":
        amount = int(request.POST["amount"])

        if amount <= remaining * 0.3:
            message = "今日は使ってOK 🌿"
        elif amount <= remaining:
            message = "うーん、今日は控えよ"
        else:
            message = "今月ちょっと厳しいかも 😇"

        # 支出登録
        Expense.objects.create(price=amount, title="今日の支出")

        # 今日の支出に応じて木を育てる
        if amount == 0:
            tree.level += 1
        elif amount > remaining * 0.3:
            tree.level = max(0, tree.level - 1)

        tree.save()

    # 木の成長をビューに渡す
    tree_stage = "🪴"  # デフォルト
    if tree.level >= 15:
        tree_stage = "💰🌳"
    elif tree.level >= 7:
        tree_stage = "🌿"
    elif tree.level >= 3:
        tree_stage = "🍃"
    elif tree.level >= 1:
        tree_stage = "🌱"

    # 木のレベルに応じたCSSクラスを計算（テンプレート用）
    tree_level = min(6, max(1, (tree.level // 3) + 1))

    return render(request, "money/index.html", {
        "remaining": remaining,
        "message": message,
        "tree_stage": tree_stage,
        "percent": int((remaining / budget.amount) * 100) if budget else 0,
        "tree_level": tree_level,  # ここで渡す
        "expenses": Expense.objects.order_by('-created_at')[:10],  # 支出履歴
    })