from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403, handler404
from exceptions.views import error401, error404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('messageservice.urls')),
]

# handler401 = error401
handler404 = error404


