from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Todo

# TODOフォーム
class TodoForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = Todo
        fields = ["title", "description", "due_date", "is_completed"]

# ユーザー新規登録フォーム
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label="メールアドレス")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")