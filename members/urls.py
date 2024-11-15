from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    path('add/', views.add_member, name='add_member'),
]
