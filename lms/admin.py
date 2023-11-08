from django.contrib import admin
from .models import User, Category, Lessons, Test, Question, Options

# Register your models here.

admin.site.register(Category)
admin.site.register(Lessons)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Options)
