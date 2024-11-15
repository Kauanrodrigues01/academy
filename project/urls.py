from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_panel.urls')),
    path('users/', include('users.urls')),
    path('members/', include('members.urls')),
]
