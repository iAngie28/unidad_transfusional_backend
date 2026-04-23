from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)
from usuarios.views.auth_views import LoginView, RegistroView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view(), name='login_global'),
    path('api/registro/', RegistroView.as_view(), name='registro'),
    path('health/', lambda r: HttpResponse("OK"), name='health'),

    # DOCUMENTACIÓN API (drf-spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]