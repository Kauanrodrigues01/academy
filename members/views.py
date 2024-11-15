from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberForm

@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro adicionado com sucesso!')
            return redirect('admin_painel:members')
        else:
            messages.error(request, 'Erro ao adicionar o membro. Verifique os dados e tente novamente.')
            return redirect('admin_painel:members')
    
    return redirect('admin_painel:members')
