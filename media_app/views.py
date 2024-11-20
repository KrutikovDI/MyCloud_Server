import os
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.utils import timezone

from media_app.models import Media
from media_app.serializers import MediaSerializer

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.none()
    serializer_class = MediaSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        other_user_id = self.request.query_params.get('user')
        if other_user_id:
            return Media.objects.filter(user=other_user_id)
        else:
            return Media.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'], url_path='rename')
    def renameFile(self, request, pk=None):
        try:
            if request.user.is_superuser:
                document = Media.objects.get(pk=pk)
            else:
                document = Media.objects.get(pk=pk, user=request.user)
        except Media.DoesNotExist:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        new_name = request.data.get('newName')
        if not new_name:
            return Response({"error": "New name not provided"}, status=status.HTTP_400_BAD_REQUEST)
        old_file_path = document.media.path
        file_extension = os.path.splitext(old_file_path)[1]
        new_file_name = f'{new_name}{file_extension}'
        new_file_path = os.path.join(settings.MEDIA_ROOT, 'documents', new_file_name)
        if not os.path.exists(old_file_path):
            return Response({"error": "File does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if os.path.exists(new_file_path):
            return Response({"error": "File with the new name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            os.rename(old_file_path, new_file_path)
            document.media.name = f'documents/{new_file_name}'   
            document.save()
            return Response({"message": "File renamed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['delete'], url_path='delete')
    def deleteFile(self, request, pk=None):
        try:
            if request.user.is_superuser:
                print(f'is_superuser {Media.objects.get(pk=pk)}')
                document = Media.objects.get(pk=pk)
            else:
                print(f'user {Media.objects.get(pk=pk, user=request.user)}')
                document = Media.objects.get(pk=pk, user=request.user)
        except Media.DoesNotExist:
            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)
        file_path = document.media.path
        if os.path.exists(file_path):
            os.remove(file_path)
        document.delete()
        return Response({"message": "File deleted successfully"}, status=status.HTTP_200_OK)

def download_file(request, uuid):
    media_file = get_object_or_404(Media, link=uuid)
    media_file.last_downloaded = timezone.now()
    media_file.save(update_fields=['last_downloaded'])
    try:
        return FileResponse(media_file.media.open('rb'), as_attachment=True)
    except FileNotFoundError:
        raise Http404("Файл не найден")