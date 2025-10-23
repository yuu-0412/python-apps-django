from django.db import models

class Todo(models.Model):
    title = models.CharField("タスク名", max_length=255)
    description = models.TextField("詳細", blank=True, null=True)
    due_date = models.DateField("期限日", null=True, blank=True)
    is_completed = models.BooleanField("完了", default=False)
    created_at = models.DateTimeField("登録日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return self.title