from django.db import models

# Create your models here.

class Users(models.Model):
    fullName = models.CharField(max_length=50)
    login = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=20)
    admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.login