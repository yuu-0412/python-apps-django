from django import forms
from .models import ClockPhoto

class ClockPhotoForm(forms.ModelForm):
    class Meta:
        model = ClockPhoto
        fields = ["image"]