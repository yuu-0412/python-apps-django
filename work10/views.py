from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Todo
from .forms import TodoForm


# ========================
# TODO一覧
# ========================
@login_required
def todo_list(request):
    sort = request.GET.get("sort", "created")
    filter_mode = request.GET.get("filter", "all")
    qs = Todo.objects.filter(user=request.user)

    # フィルタ（未完了・完了）
    if filter_mode == "active":
        qs = qs.filter(is_completed=False)
    elif filter_mode == "completed":
        qs = qs.filter(is_completed=True)

    # 並び替え（締切 or 作成日）
    if sort == "due":
        qs = qs.order_by(F("due_date").asc(nulls_last=True))
    else:
        qs = qs.order_by("-created_at")

    today = timezone.localdate()

    context = {
        "todos": qs,
        "today": today,
        "sort": sort,
        "filter_mode": filter_mode,
    }
    return render(request, "work10/todo_list.html", context)


# ========================
# TODO作成
# ========================
@login_required
def todo_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect("work10:todo_list")
    else:
        form = TodoForm()
    return render(request, "work10/todo_form.html", {"form": form, "is_create": True})


# ========================
# TODO編集
# ========================
@login_required
def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("work10:todo_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "work10/todo_form.html", {"form": form, "todo": todo, "is_create": False})


# ========================
# TODO削除
# ========================
@login_required
def todo_delete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    if request.method == "POST":
        if "confirm_delete" in request.POST:
            todo.delete()
        return redirect("work10:todo_list")
    return render(request, "work10/todo_confirm_delete.html", {"todo": todo})


# ========================
# 完了/未完了切替
# ========================
@login_required
def toggle_complete(request, pk):
    todo = get_object_or_404(Todo, pk=pk, user=request.user)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect("work10:todo_list")


# ========================
# ユーザー登録（サインアップ）
# ========================
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 登録後に自動ログイン
            return redirect("work10:todo_list")
    else:
        form = UserCreationForm()
    return render(request, "work10/signup.html", {"form": form})

