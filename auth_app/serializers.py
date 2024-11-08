from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password
from auth_app.models import Users


class UsersSerializer(serializers.ModelSerializer):
    media_count = serializers.IntegerField(read_only=True)
    media_size = serializers.IntegerField(read_only=True)
    class Meta:
        model = Users
        fields = ['fullName', 'login', 'email', 'password', 'is_superuser', 'media_count', 'media_size', 'id']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    login = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Users
        fields = ['login', 'password', 'is_superuser']

    def validate(self, data):
        login = data.get("login")
        password = data.get("password")
        is_superuser = data.get('is_superuser')
        try:
            user = Users.objects.get(login=login)
        except Users.DoesNotExist:
            raise serializers.ValidationError({'error': "Пользователь с таким логином не найден."})

        if not check_password(password, user.password):
            raise serializers.ValidationError({'error': "Неверный пароль"})
        
        if user.is_superuser == False and is_superuser == True:
            raise serializers.ValidationError({'error': "Прав администратора нет"})

        data["user"] = user
        return data