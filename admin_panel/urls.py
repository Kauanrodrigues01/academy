from django.urls import path
from . import views

app_name = 'admin_painel'

urlpatterns = [
    path('', views.home, name='home'),
    path('members/', views.members, name='members'),
    path('members/edit/<int:id>/', views.edit_member_view, name='edit_member_view'),
]
