from django.contrib import admin
from media_app.models import Media

# Register your models here.

@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'media', 'uploaded_at', 'comment']
    list_filter = ['user',]
    search_fields = ('media',)
    ordering = ('-uploaded_at',)
    list_filter = ('uploaded_at',)