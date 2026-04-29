from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from apps.users.serializers.auth_serializers import UserSerializer
from django.contrib.auth import authenticate

class CustomLoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = authenticate(
                username=request.data.get('username'),
                password=request.data.get('password')
            )
            user_data = UserSerializer(user).data
            
            return Response({
                "success": True,
                "message": "Login exitoso",
                "data": {
                    **serializer.validated_data,
                    "user": user_data
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "message": "Credenciales inválidas",
                "errors": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)