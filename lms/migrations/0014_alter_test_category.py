# Generated by Django 4.2.7 on 2023-11-12 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0013_testcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.testcategory'),
        ),
    ]