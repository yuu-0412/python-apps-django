
from django import forms
from django.core.exceptions import ValidationError
from .models import ClockPhoto


class ClockPhotoForm(forms.ModelForm):

    class Meta:
        model = ClockPhoto
        fields = ["image"]

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if image:
            # 画像サイズを5MBまでに制限
            if image.size > 5 * 1024 * 1024:
                raise ValidationError(
                    "画像サイズは5MB以下にしてください。"
                )

        return image
