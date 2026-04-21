from django.db import models

# 今月の予算
class MonthlyBudget(models.Model):
    month = models.CharField(max_length=7)  # "2026-01" の形式など
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.month} - {self.amount}円"


# 支出の記録
class Expense(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.price}円"


# 木の成長状態
class TreeStatus(models.Model):
    level = models.IntegerField(default=0)  # 0:種, 1:芽, 2:小さい木, 3:大きい木, 4:金のなる木
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        levels = ["種", "芽", "小さい木", "大きい木", "金のなる木"]
        return levels[self.level] if self.level < len(levels) else "未知の状態"