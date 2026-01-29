from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from .models import Usuario
from .serializers import UsuarioSerializer, LoginUsuarioSerializer
from .permissions import IsAdminPermission, IsStaffPermission, IsAdminOrOwnerStaffPermission

# Create your views here.
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminOrOwnerStaffPermission]
        elif self.action in ['create', 'list']:
            permission_classes = [IsAdminPermission]
        else:
            permission_classes = [IsStaffPermission]
        return [permission() for permission in permission_classes]
    
    @action(detail=True, methods=['get'])
    def me(self, request):
        usuario = request.user
        serializer = self.get_serializer(usuario)
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginUsuarioSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)

            response = Response({
                "user": UsuarioSerializer(user).data}, status=status.HTTP_200_OK)
            response.set_cookie(key="access_token",
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            response.set_cookie(key="refresh_token",
                                value=str(refresh_token),
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except Exception as e:
                return Response({"error": "Token inválido:" + str(e)}, status=status.HTTP_400_BAD_REQUEST)
        response = Response({"message": "Logout concluído"}, status=status.HTTP_200_OK)
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response
    
class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "RefreshToken não foi fornecido"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({"message": "AccessToken recarregado!"}, status=status.HTTP_200_OK)
            response.set_cookie(key="access_token",
                                value=access_token,
                                httponly=True,
                                secure=True,
                                samesite="None")
            return response
        except InvalidToken:
            return Response({"error": "Token Inválido"}, status=status.HTTP_401_UNAUTHORIZED)