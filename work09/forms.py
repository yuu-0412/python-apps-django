from django import forms
from .models import Todo

class TodoForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Todo
        fields = ["title", "description", "due_date", "is_completed"]