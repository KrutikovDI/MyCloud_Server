from django.db import models
from auth_app.models import Users

# Create your models here.

class Media(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='documents/')
    comment = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.media.name