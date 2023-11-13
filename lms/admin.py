from django.contrib import admin
from .models import User, Classrooms, Lessons, Test, Question, Options, UserAnswer, ProfileUser

# Register your models here.

admin.site.register(Classrooms)
admin.site.register(Lessons)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Options)
admin.site.register(UserAnswer)
admin.site.register(ProfileUser)
