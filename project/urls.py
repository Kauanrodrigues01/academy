from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_panel.urls')),
    path('users/', include('users.urls')),
    path('members/', include('members.urls')),
]

if settings.DEBUG:  # Somente em modo de desenvolvimento
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]