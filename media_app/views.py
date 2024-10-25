import os
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import viewsets
from rest_framework.decorators import action

from media_app.models import Media
from media_app.serializers import MediaSerializer

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    # def create(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        # print(f"Данные запроса (POST): {request.data}")
        # print(f"файл запроса: {request.FILES}")
        # Проверка валидности данных
        # if serializer.is_valid():
            # serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        # else:
            # Вывод ошибок валидации в консоль и отправка их в ответе
            # print(f"Ошибки валидации: {serializer.errors}")
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # def create(self, request, *args, **kwargs):
    #     print(f"Данные запроса (POST): {request.data}")
    #     print(f"пользователь: {request.data.get('user')}")
    #     print(f"Файл: {request.data.get('media')}")
    #     print(f"комментирий: {request.data.get('comment')}")
    #     # logging.debug(f"Received data: {request.data}")
    #     return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='rename')
    def renameFile(self, request, pk=None):
        document = self.get_object()
        new_name = request.data.get('newName')
        if not new_name:
            return Response({"error": "New name not provided"}, status=status.HTTP_400_BAD_REQUEST)
        old_file_path = document.media.path
        file_extension = os.path.splitext(old_file_path)[1]  # Получаем расширение файла
        new_file_name = f"{new_name}{file_extension}"
        new_file_path = os.path.join(settings.MEDIA_ROOT, 'documents', new_file_name)
        try:
            os.rename(old_file_path, new_file_path)
            document.media.name = f'documents/{new_file_name}'
            document.save()
            return Response({"message": "File renamed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)