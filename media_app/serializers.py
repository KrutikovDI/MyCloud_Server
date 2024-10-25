from rest_framework import serializers
from media_app.models import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'user', 'media', 'comment', 'uploaded_at']
        read_only_fields = ['uploaded_at']