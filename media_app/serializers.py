from rest_framework import serializers
from django.urls import reverse

from media_app.models import Media

class MediaSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    class Meta:
        model = Media
        fields = ['id', 'media', 'comment', 'uploaded_at', 'size', 'download_url', 'last_downloaded']
        read_only_fields = ['uploaded_at']

    def get_download_url(self, obj):
        request = self.context.get('request')
        path = reverse('download_file', kwargs={'uuid': obj.link})
        return request.build_absolute_uri(path) if request else path