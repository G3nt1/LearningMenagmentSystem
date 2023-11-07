from django.contrib import admin
from .models import User, Category, Lessons, Test

# Register your models here.

admin.site.register(Category)
admin.site.register(Lessons)
admin.site.register(Test)