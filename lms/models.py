from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField


# Create your models here.
class ProfileUser(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username.first_name


class Classrooms(models.Model):
    name = models.CharField(max_length=255, unique=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

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
    category = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Test(models.Model):
    category = models.ForeignKey(Classrooms, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, max_length=255, null=True)
    max_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User, related_name='tests', blank=True)

    def __str__(self):
        return self.name


def validate_non_negative(value):
    if value < 1:
        raise ValidationError("Points cannot be a negative value.")
    elif value > 10:
        raise ValidationError("Points cannot be a negative value.")


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)
    points = models.IntegerField(default=1, validators=[validate_non_negative])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Options(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Options, on_delete=models.CASCADE, null=True)  # Allow null values
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_correct:
            self.points_earned = self.question.points
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.question.name}: {self.answer.text}"

    class Meta:
        unique_together = ('user', 'test', 'question')
