from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # Django auth URLs
    path('', include('cycles.urls')),
]

handler400 = 'cycles.views.bad_request'
handler403 = 'cycles.views.permission_denied'
handler404 = 'cycles.views.page_not_found'
handler500 = 'cycles.views.server_error'
