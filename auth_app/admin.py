from django.contrib import admin
from auth_app.models import Users

# Register your models here.

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['fullName', 'login', 'email', 'password', ]
    list_filter = []