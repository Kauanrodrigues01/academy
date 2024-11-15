from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from members.forms import MemberForm
from members.models import Member

# Create your views here.
@login_required
def home(request):
    return render(request, 'admin_painel/pages/home.html')

@login_required
def members(request):
    form = MemberForm()
    context = {
        'form': form,
        'members': Member.objects.all()
    }
    return render(request, 'admin_painel/pages/members.html', context)
