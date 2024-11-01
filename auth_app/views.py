import json
import logging
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError


from auth_app.models import Users
from auth_app.serializers import UsersSerializer
from auth_app.serializers import UserLoginSerializer

logger = logging.getLogger(__name__)

class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['post'], url_path='login', permission_classes=[AllowAny])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.validated_data["user"]
            token, create = Token.objects.get_or_create(user=user)
            return Response({
                'is_active': user.is_active,
                'fullName': user.fullName,
                'login': user.login,
                'token': token.key,
                }, status=status.HTTP_200_OK)
        except Exception as error:
            logger.error(f"Ошибка при входе: {error}")
            return Response({"error": ["Произошла непредвиденная ошибка на сервере."]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=False, methods=['post'], url_path='register', permission_classes=[AllowAny])
    def register(self, request):
        serializer = UsersSerializer(data = request.data)
        try:
            if serializer.is_valid():
                user = serializer.save()
                token, create = Token.objects.get_or_create(user=user)
                return Response({
                    'is_active': user.is_active,
                    'fullName': user.fullName,
                    'login': user.login,
                    'token': token.key,
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            logger.error(f"Ошибка при входе: {error}")
            return Response({"error": ["Произошла непредвиденная ошибка на сервере."]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)