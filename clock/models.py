# clock/models.py
from django.db import models

class ClockPhoto(models.Model):
    image = models.ImageField(upload_to='photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id}"


class ClockSetting(models.Model):
    # 背景に設定されている写真を1つ記録
    selected_photo = models.ForeignKey(
        ClockPhoto, null=True, blank=True, on_delete=models.SET_NULL
        
    )

    def __str__(self):
        return "Clock Setting"