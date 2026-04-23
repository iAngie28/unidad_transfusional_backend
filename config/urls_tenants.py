from django.urls import path
from usuarios.views.auth_views import LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth Endpoints
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]