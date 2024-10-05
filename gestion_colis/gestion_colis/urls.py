from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('colis/', include('colis.urls')),  # Inclut les routes de l'application `colis`
]
