from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('add/', views.add_member, name='add_member'),
    path('delete/<int:id>/', views.delete_member, name='delete_member'),
    path('edit/<int:id>/update/', views.edit_member_update, name='edit_member_update'),
]
