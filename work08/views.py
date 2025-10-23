

from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo
from .forms import MemoForm

def memo_list(request):
    memos = Memo.objects.all().order_by('-updated_at')
    return render(request, 'work08/memo_list.html', {'memos': memos})

def memo_create(request):
    memo = Memo.objects.create()
    return redirect('memo_edit', memo_id=memo.id)

def memo_edit(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id)
    if request.method == 'POST':
        form = MemoForm(request.POST, request.FILES, instance=memo)
        if form.is_valid():
            form.save()
            return redirect('memo_list')
    else:
        form = MemoForm(instance=memo)
    return render(request, 'work08/memo_edit.html', {'form': form, 'memo': memo})

def memo_delete(request, memo_id):
    memo = get_object_or_404(Memo, id=memo_id)
    memo.delete()
    return redirect('memo_list')