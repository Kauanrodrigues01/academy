from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from members.forms import MemberPaymentForm, PaymentForm, MemberEditForm
from .models import ActivityLog
from members.models import Member, Payment
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from calendar import month_name

# Create your views here.
@login_required
def home(request):
    current_month = now().month
    current_year = now().year
    
    
    count_new_members_in_month = Member.objects.filter( created_at__month=current_month, created_at__year=current_year).count()
    value_total_month = Payment.get_current_month_profit()
    recent_activities = ActivityLog.objects.all().order_by('-id')[:20]
    
    context = {
        'count_members_actives': Member.objects.filter(is_active=True).count(),
        'count_members_inactives': Member.objects.filter(is_active=False).count(),
        'count_new_members_in_month': count_new_members_in_month,
        'value_total_month': value_total_month,
        'recent_activities': recent_activities
    }
    return render(request, 'admin_panel/pages/home.html', context)

@login_required
def members(request):
    form_data_add_member = request.session.get('form_data_add_member')
    
    if form_data_add_member:
        form = MemberPaymentForm(form_data_add_member)
        request.session['form_data_add_member'] = None
    else:
        form = MemberPaymentForm()
        
    context = {
        'form': form,
        'members': Member.objects.all().order_by('-id')
    }
    return render(request, 'admin_panel/pages/members.html', context)

@login_required
def edit_member_view(request, id):
    member = get_object_or_404(Member, id=id)

    form_data_edit_member = request.session.get('form_data_edit_member')
    
    if form_data_edit_member:
        form = MemberEditForm(form_data_edit_member, instance=member)
        request.session['form_data_edit_member'] = None 
    else:
        form = MemberEditForm(instance=member)

    return render(request, 'admin_panel/pages/member_edit.html', {'form': form, 'member': member})


@login_required
def add_payment_view(request, id):
    member = get_object_or_404(Member, id=id)
    form_data_add_payment = request.session.get('form_data_add_payment')
    
    if form_data_add_payment:
        form = PaymentForm(form_data_add_payment)
    else:
        form = PaymentForm()
    
    context = {
        'form': form,
        'member': member
    }
    
    return render(request, 'admin_panel/pages/add_payment.html', context)


@login_required
def finance(request):
    current_year_profit = Payment.get_current_year_profit()
    current_month_profit = Payment.get_current_month_profit()
    
    months_profit = {
        'Janeiro': Payment.get_monthly_profit(1),
        'Fevereiro': Payment.get_monthly_profit(2),
        'Março': Payment.get_monthly_profit(3),
        'Abril': Payment.get_monthly_profit(4),
        'Maio': Payment.get_monthly_profit(5),
        'Junho': Payment.get_monthly_profit(6),
        'Julho': Payment.get_monthly_profit(7),
        'Agosto': Payment.get_monthly_profit(8),
        'Setembro': Payment.get_monthly_profit(9),
        'Outubro': Payment.get_monthly_profit(10),
        'Novembro': Payment.get_monthly_profit(11),
        'Dezembro': Payment.get_monthly_profit(12),
    }
        
    month_with_highest_profit = max(months_profit, key=lambda month: months_profit[month])
    
    recents_payments = Payment.objects.order_by('-id')[:12]
    
    
    context = {
        'current_year_profit': current_year_profit,
        'current_month_profit': current_month_profit,
        'months_profit': months_profit,
        'month_with_highest_profit': month_with_highest_profit,
        'recents_payments': recents_payments
    }
    
    
    
    
    return render(request, 'admin_panel/pages/finance.html', context)