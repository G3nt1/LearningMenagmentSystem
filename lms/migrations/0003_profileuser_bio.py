# Generated by Django 4.2.7 on 2023-11-13 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_profileuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileuser',
            name='bio',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
