# Generated by Django 4.2.7 on 2023-11-12 14:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lms', '0014_alter_test_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='LessonCategory',
        ),
    ]