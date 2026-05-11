from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views.auth_views import CustomLoginView
from .views.rol_views import RolViewSet
from .views.user_views import UserViewSet

router = DefaultRouter()
router.register(r'roles', RolViewSet, basename='roles')
router.register(r'usuarios', UserViewSet, basename='usuarios')

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
