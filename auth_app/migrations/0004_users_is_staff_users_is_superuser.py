# Generated by Django 5.1.2 on 2024-10-29 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0003_users_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='users',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
