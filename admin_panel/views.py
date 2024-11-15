from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def painel_admin(request):
    return render(request, 'admin_painel/pages/home.html')