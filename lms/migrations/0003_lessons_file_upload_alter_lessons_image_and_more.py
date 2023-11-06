# Generated by Django 4.2.7 on 2023-11-06 02:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_lessons_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessons',
            name='file_upload',
            field=models.FileField(blank=True, null=True, upload_to='media/files'),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='lessons',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/%Y/%m/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]