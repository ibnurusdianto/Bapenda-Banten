from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # bagian untuk melakukan pemanggilan pada semua path yang di folder website
    path('', include('website.urls')),
]
