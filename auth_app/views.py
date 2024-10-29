import json
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError


from auth_app.models import Users
from auth_app.serializers import UsersSerializer
from auth_app.serializers import UserLoginSerializer


class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        try:
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response({
                'fullName': user.fullName,
                'login': user.login,
                'refresh': str(refresh),
                'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response({"error": ["Произошла непредвиденная ошибка на сервере."]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)