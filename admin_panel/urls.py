from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.home, name='home'),
    
    path('members/', views.members, name='members'),
    path('members/edit/<int:id>/', views.edit_member_view, name='edit_member_view'),
    path('members/add-payment-view/<int:id>/', views.add_payment_view, name='add_payment_view'),
    
    path('finance/', views.finance, name='finance'),
    
    path('generate-report/', views.generate_pdf_report, name='generate_pdf_report'),
]
