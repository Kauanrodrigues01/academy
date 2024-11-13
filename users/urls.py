from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    
    path('reset-password/', views.reset_password_view, name='reset-password-view'),
    path('send-request-reset-password/', views.send_request_reset_password, name='send-request-reset-password'),
    
    path('reset-confirm/<uidb64>/<token>/', views.reset_confirm_view, name='reset-confirm-view'),
    path('reset-confirm-set/', views.reset_confirm_set, name='reset-confirm-set'),
    
    path('', views.home, name='home')
]
