from django.urls import path
from . import views

app_name = 'admin_painel'

urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),
]
