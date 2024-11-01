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
        return Media.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'], url_path='rename')
    def renameFile(self, request, pk=None):
        document = self.get_object()
        new_name = request.data.get('newName')
        if not new_name:
            return Response({"error": "New name not provided"}, status=status.HTTP_400_BAD_REQUEST)
        old_file_path = document.media.path
        file_extension = os.path.splitext(old_file_path)[1]
        new_file_name = f'{new_name}{file_extension}'
        new_file_path = os.path.join(settings.MEDIA_ROOT, 'documents', new_file_name)
        print(old_file_path)
        print(new_file_path)
        try:
            os.rename(old_file_path, new_file_path)
            document.media.name = f'documents/{new_file_name}'
            document.save()
            return Response({"message": "File renamed successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def download_file(request, uuid):
    media_file = get_object_or_404(Media, link=uuid)
    media_file.last_downloaded = timezone.now()
    media_file.save(update_fields=['last_downloaded'])
    try:
        return FileResponse(media_file.media.open('rb'), as_attachment=True)
    except FileNotFoundError:
        raise Http404("Файл не найден")