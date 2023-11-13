from django.shortcuts import render, redirect, get_object_or_404
from lms.models import Lessons, Classrooms
from lms.forms import CreateLessonsForm, CreateClassroomForm, Classrooms
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request, category_name=None):
    category = Classrooms.objects.all()
    if category_name:
        lessons = Lessons.objects.filter(category__name=category_name).order_by('-created_at')
    else:
        lessons = Lessons.objects.all().order_by('-created_at')

    user = request.user
    context = {
        'category': category_name,
        'selected_category': category,
        'lessons': lessons,
        'user': user,
    }

    return render(request, 'home.html', context)




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
            form = CreateLessonsForm()
        content = {'form': form}  # Include lessons in the content
        return render(request, 'lesson/create_new_lesson.html', content)


def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = CreateLessonsForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.creator = request.user
            lesson.save()
            return redirect('home')
    else:
        form = CreateLessonsForm(instance=lesson)
    content = {'form': form}  # Include lessons in the content
    return render(request, 'lesson/edit_lesson.html', content)


def lesson_details(request, lesson_id):
    lesson = Lessons.objects.filter(id=lesson_id)
    return render(request, 'lesson/details_lesson.html', {'lesson': lesson})


def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.user != lesson.creator:
        return redirect('home')
    if request.method == 'POST':
        lesson.delete()
        return redirect('home')

    return render(request, 'lesson/delete_lesson.html', {'lesson': lesson})


def create_classroom(request):
    if request.method == 'POST':
        form = CreateClassroomForm(request.POST)
        if form.is_valid():
            classroom = form.save(commit=False)
            classroom.creator = request.user
            classroom.save()
            return redirect('home')
    else:
        form = CreateClassroomForm()
        return render(request, 'lesson/create_classroom.html', {'form': form})

