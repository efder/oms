from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404, handler500
from exceptions.views import error404, error500

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('messageservice.urls')),
]

handler404 = error404
handler500 = error500


