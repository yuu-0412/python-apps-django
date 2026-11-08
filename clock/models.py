
from django.db import models


class ClockPhoto(models.Model):
    # 利用者を識別するCookieのID
    owner_id = models.CharField(
        max_length=64,
        db_index=True
    )

    # アップロードした写真
    image = models.ImageField(upload_to='photos/')

    # アップロード日時
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.id}"


class ClockSetting(models.Model):
    # 利用者を識別するCookieのID
    owner_id = models.CharField(
        max_length=64,
        unique=True,
        db_index=True
    )

    # 選択中の背景写真
    selected_photo = models.ForeignKey(
        ClockPhoto,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Clock Setting: {self.owner_id}"
