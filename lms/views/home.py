import markdown
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from lms.models import Lessons, Classrooms, ProfileUser
from lms.forms import CreateLessonsForm, CreateClassroomForm, Classrooms
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    classrooms = Classrooms.objects.all()
    lessons = Lessons.objects.filter(Q(users=request.user) | Q(creator=request.user)).distinct()
    if lessons.exists():
        # Assuming you want to get the description of the first lesson
        html = markdown.markdown(lessons[0].description, extensions=[
            'markdown.extensions.fenced_code',
            'markdown.extensions.admonition',
            'markdown.extensions.tables',
            'fenced_code',
        ])
    else:
        html = ""
    # Check if a classroom is selected in the request
    selected_classroom_id = request.GET.get('classroom')
    selected_classroom = None

    if selected_classroom_id:
        selected_classroom = get_object_or_404(Classrooms, id=selected_classroom_id)

        lessons = lessons.filter(category=selected_classroom)

    context = {'lessons': lessons, 'classrooms': classrooms, 'selected_classroom': selected_classroom}

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
                form.save_m2m()

                return redirect('home')
        else:
            form = CreateLessonsForm()
        content = {'form': form}
        return render(request, 'lesson/create_new_lesson.html', content)


def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lessons, id=lesson_id)
    if request.method == 'POST':
        form = CreateLessonsForm(request.POST, request.FILES, instance=lesson)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.creator = request.user
            lesson.save()
            form.save_m2m()
            return redirect('details_lesson', lesson_id=lesson.id)
    else:
        form = CreateLessonsForm(instance=lesson)
    content = {'form': form}  # Include lessons in the content
    return render(request, 'lesson/edit_lesson.html', content)


def lesson_details(request, lesson_id):
    lesson = Lessons.objects.get(id=lesson_id)
    html = markdown.markdown(lesson.description, extensions=[
        'markdown.extensions.fenced_code',
        'markdown.extensions.admonition',
        'markdown.extensions.tables',
        'fenced_code',
    ])

    return render(request, 'lesson/details_lesson.html', {'lesson': lesson,'html': html })

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

# def search(request):
