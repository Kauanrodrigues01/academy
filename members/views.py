from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MemberEditForm, MemberPaymentForm, PaymentForm
from .models import Member
from django.shortcuts import render, get_object_or_404

@login_required
def add_member(request):
    request.session['form_data_add_member'] = request.POST
    if request.method == 'POST':
        form = MemberPaymentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Membro adicionado com sucesso!')
            return redirect('admin_panel:members')
        else:
            messages.error(request, 'Erro ao adicionar o membro. Verifique os dados e tente novamente.')
            return redirect('admin_panel:members')
    
    return redirect('admin_panel:members')

@login_required
def delete_member(request, id):
    member = Member.objects.get(id=id)
    member.delete()
    messages.success(request, 'Membro deletado com sucesso!')
    return redirect('admin_panel:members')


@login_required
def edit_member_update(request, id):
    member = get_object_or_404(Member, id=id)
    request.session['form_data_edit_member'] = request.POST

    if request.method == 'POST':
        form = MemberEditForm(request.POST, instance=member)

        if form.is_valid():
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            full_name = form.cleaned_data['full_name']
            is_active = form.cleaned_data['is_active'] 
            
            member.email = email
            member.phone = phone
            member.full_name = full_name
            member.is_active = is_active
            member.save()
            messages.success(request, 'Membro atualizado com sucesso!')
            return redirect('admin_panel:members')
        else:
            messages.error(request, 'Erro ao atualizar o membro. Verifique os dados e tente novamente.')
            return redirect('admin_panel:edit_member_view', id=id) 

@login_required
def add_payment(request, id):
    member = get_object_or_404(Member, id=id)
    
    request.session['form_data_add_payment'] = request.POST
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        
        if form.is_valid():
            form.save(member=member)
            messages.success(request, 'Pagamento adicionado com sucesso!')
            del request.session['form_data_add_payment']
            return redirect('admin_panel:members')
        else:
            messages.error(request, 'Erro ao adicionar pagamento. Verifique os dados e tente novamente.')
            return redirect('admin_panel:add_payment_view', id=id)
    else:
        return redirect('admin_panel:add_payment_view', id=id)

        