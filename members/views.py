from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberForm, MemberEditForm
from .models import Member
from django.shortcuts import render, get_object_or_404

@login_required
def add_member(request):
    request.session['form_data_add_member'] = request.POST
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

@login_required
def delete_member(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.success(request, 'Membro deletado com sucesso!')
    return redirect('admin_painel:members')


@login_required
def edit_member_update(request, id):
    member = get_object_or_404(Member, id=id)
    request.session['form_data_edit_member'] = request.POST

    if request.method == 'POST':
        form = MemberEditForm(request.POST, instance=member)

        if form.is_valid():
            form.save()  
            messages.success(request, 'Membro atualizado com sucesso!')
            return redirect('admin_painel:members')
        else:
            messages.error(request, 'Erro ao atualizar o membro. Verifique os dados e tente novamente.')
            return redirect('admin_painel:edit_member_view', id=id) 
