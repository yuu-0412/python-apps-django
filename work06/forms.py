from django import forms

class ReiwaForm(forms.Form):
    year = forms.IntegerField(
        label="令和何年？",min_value=1
    )