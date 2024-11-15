from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_admin, name='painel_admin'),
]
