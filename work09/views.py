from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import F
from .models import Todo
from .forms import TodoForm

def todo_list(request):
    # クエリパラメータ: sort=created|due, filter=all|active
    sort = request.GET.get("sort", "created")
    filter_mode = request.GET.get("filter", "all")

    qs = Todo.objects.all()

    if filter_mode == "active":
        qs = qs.filter(is_completed=False)

    if sort == "due":
        # due_date が NULL のものは末尾に回す（Djangoではannotateしてソート可能）
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
    return render(request, "work09/todo_list.html", context)

def todo_create(request):
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("work09:todo_list")
    else:
        form = TodoForm()
    return render(request, "work09/todo_form.html", {"form": form, "is_create": True})

def todo_edit(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        if "delete" in request.POST:
            todo.delete()
            return redirect("work09:todo_list")
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("work09:todo_list")
    else:
        form = TodoForm(instance=todo)
    return render(request, "work09/todo_form.html", {"form": form, "todo": todo, "is_create": False})

# optional: delete via dedicated view (here we handle delete in edit form)


def toggle_complete(request, todo_id):
    if request.method == "POST":
        todo = get_object_or_404(Todo, pk=todo_id)
        todo.is_completed = not todo.is_completed
        todo.save()
    return redirect('work09:todo_list')

def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == "POST":
        todo.delete()
        return redirect("work09:todo_list")
    return render(request, "work09/todo_confirm_delete.html", {"todo": todo})