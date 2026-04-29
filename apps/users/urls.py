from django.urls import path
from .views.auth_views import CustomLoginView # El que creamos antes
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]