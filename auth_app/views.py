import json
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ViewSet, ModelViewSet


from auth_app.models import Users
from auth_app.serializers import UsersSerializer

# def chat_enter(request):
#     message = 'вы вошли в систему'
#     print('вы вошли в систему')
#     return HttpResponse(message)

# def users_list(request):
#     users = Users.objects.all()
#     return HttpResponse(users)

# def user_login(request, user_login):
#     user = get_object_or_404(Users, login=user_login)
#     return HttpResponse(user)

@api_view(['POST'])
def chat_enter(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    print(data_json)
    userRegistration = Users.objects.get(login=data_json['login'])
    serializer_user = UsersSerializer(userRegistration)
    if data_json['password'] == serializer_user.data['password'] and data_json['admin'] == serializer_user.data['admin']:
        return Response(serializer_user.data, 200)
    elif data_json['password'] != serializer_user.data['password']:
        return Response(status=401)
    elif data_json['admin'] != serializer_user.data['admin']:
        return Response(status=402)
    
    # print(serializer_user.data['password'])
    # print(data_json['password'])
    # print(userReg)
    # return Response(serializer_user.data)
    

# @api_view(['GET'])
# def users_list(request):
#     users = Users.objects.all()
#     serializer_user = UsersSerializer(users, many=True)
#     print('получен запрос на users')
#     return Response(serializer_user.data)

# class UserView(ListAPIView):
#     queryset = Users.objects.all()
#     serializer_class = UsersSerializer

class UsersViewSet(ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    filterset_fields = ['fullName', 'password',]