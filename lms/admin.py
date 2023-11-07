from django.contrib import admin
from .models import User, Classroom, Lessons, Test

# Register your models here.

admin.site.register(Classroom)
admin.site.register(Lessons)
admin.site.register(Test)