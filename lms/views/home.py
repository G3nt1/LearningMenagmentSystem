from django.shortcuts import render, redirect
from lms.models import Lessons
from lms.forms import CreateLessonsForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    lessons = Lessons.objects.all()
    return render(request, 'home.html', {'lessons': lessons})


@login_required
def create_lesson(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateLessonsForm(request.POST, request.FILES)
            if form.is_valid():
                lesson = form.save(commit=False)
                lesson.creator = request.user
                lesson.save()
                return redirect('home')
        else:
            form = CreateLessonsForm
            content = {'form': form}  # Include lessons in the content
            return render(request, 'exercises/create_new_lesson.html', content)

