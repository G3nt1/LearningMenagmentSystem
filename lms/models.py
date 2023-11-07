from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Lessons(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    file_upload = models.FileField(blank=True, null=True, upload_to='media/files')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True, null=True)
    video = models.FileField(upload_to='videos/%Y/%m/', null=True, blank=True,
                             validators=[
                                 FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Test(models.Model):
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    max_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __set__(self):
        return self.name, self.max_points, self.creator.first_name + self.creator.last_name
