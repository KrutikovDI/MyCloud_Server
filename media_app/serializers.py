from rest_framework import serializers
from media_app.models import Media

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['user', 'mudia', 'uploaded_at', 'comment']