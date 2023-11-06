from django.shortcuts import render, redirect, get_object_or_404
from lms.models import Lessons, Category
from lms.forms import CreateLessonsForm
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request, category=None):
    categories = Category.objects.all()

    if category:
        lessons = Lessons.objects.filter(category__name=category).order_by('-created_at')
    else:
        lessons = Lessons.objects.all().order_by('-created_at')

    user = request.user
    context = {
        'categories': categories,
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
            return render(request, 'exercises/create_new_lesson.html', content)


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
    return render(request, 'exercises/edit_lesson.html', content)


def lesson_details(request, lesson_id):
    lesson = Lessons.objects.filter(id=lesson_id)
    return render(request, 'exercises/details_lesson.html', {'lesson': lesson})


def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.user != lesson.creator:
        return redirect('home')
    if request.method == 'POST':
        lesson.delete()
        return redirect('home')

    return render(request, 'exercises/delete_lesson.html', {'lesson': lesson})
