from django.contrib import admin
from .models import Member, Payment
# Register your models here.

admin.site.register(Payment)
admin.site.register(Member)