# Generated by Django 4.2.7 on 2023-11-14 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_remove_question_text_big'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='options',
            name='text_big',
        ),
    ]
