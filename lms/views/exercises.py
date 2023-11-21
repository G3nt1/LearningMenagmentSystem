from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from lms.forms import CreateTestForm, CreateQuestionForm, CreateOptionFormSet
from lms.models import Test, Question, Options, Lessons, UserAnswer, Classrooms


#  Test
def tests(request):
    classrooms = Classrooms.objects.all()
    # Get the selected classroom from the request
    selected_classroom_id = request.GET.get('classroom')
    selected_classroom = None

    # If a classroom is selected, filter tests based on the selected classroom
    if selected_classroom_id:
        selected_classroom = get_object_or_404(Classrooms, id=selected_classroom_id)
        tests = Test.objects.filter(
            Q(creator=request.user) | Q(users=request.user),
            category=selected_classroom
        ).distinct()
    else:
        # If no classroom is selected, show all tests
        tests = Test.objects.filter(
            Q(creator=request.user) | Q(users=request.user)
        ).distinct()

    context = {'tests': tests, 'selected_classroom': selected_classroom, 'classrooms':classrooms}
    return render(request, 'test/show_test.html', context)



@login_required
def test_list(request):
    # Get tests created by the current user or tests with answers provided by the current user
    tests = Test.objects.filter(Q(creator=request.user) | Q(useranswer__user=request.user)).distinct()

    # Create a dictionary to store test names and unique users who took each test
    test_users_dict = {}
    for test in tests:
        # Get unique users who took this test
        users_took_test = UserAnswer.objects.filter(test=test).values_list('user__first_name',
                                                                           'user__last_name',
                                                                           'user__email').distinct()
        test_users_dict[test] = users_took_test

    return render(request, 'test/display_tests.html', {'test_users_dict': test_users_dict})


def create_test(request):
    if request.method == 'POST':
        form = CreateTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.creator = request.user
            test.save()
            form.save_m2m()  # Save the many-to-many relationships
            return redirect('tests')
    else:
        form = CreateTestForm()
    return render(request, 'test/create_new_test.html', {"form": form})


def edit_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.method == 'POST':
        form = CreateTestForm(request.POST, instance=test)
        if form.is_valid():
            test = form.save(commit=False)
            test.creator = request.user
            test.save()
            form.save_m2m()
            return redirect('tests')
    else:
        form = CreateTestForm(instance=test)
    return render(request, 'test/edit_test.html', {"form": form})


def delete_test(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    if request.user != test.creator:
        return redirect('home')
    if request.method == 'POST':
        test.delete()
        return redirect('tests')

    return render(request, 'test/delete_test.html', {"test": test})


# end test
# #########
# Questions  /////...............

def questions(request, test_id):
    question = get_object_or_404(Question, id=test_id)
    return render(request, 'question/show_question.html', test_id, {"question": question})


def create_question(request, test_id):
    test = get_object_or_404(Test, id=test_id)
    question = Question.objects.filter(test__name=test.name)
    if request.user != test.creator:
        return redirect('home')

    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        form.instance.test_id = test_id

        if form.is_valid():
            new_question = form.save()
            return redirect('create_options', question_id=new_question.id)
    else:

        form = CreateQuestionForm()
        return render(request, 'question/create_question.html', {"form": form, "test": test, "questions": question})


def edit_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    if request.user != test.creator:
        return redirect('test')
    if request.method == 'POST':

        form = CreateQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('create_question', test_id=test.id)
    else:
        form = CreateQuestionForm(instance=question)
        return render(request, 'question/edit_question.html', {"form": form, "test": test})


def delete_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test
    if request.method == 'POST':
        question.delete()
        return redirect('create_question', test_id=test.id)
    return render(request, 'question/delete_question.html', {"question": question})


# ...  Options
def create_options(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test  # Assuming Test has a ForeignKey to Question

    if request.method == 'POST':
        formset = CreateOptionFormSet(request.POST, queryset=Options.objects.none())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.question_id = question_id
                instance.save()
            return redirect('create_question', test_id=test.id)
    else:
        formset = CreateOptionFormSet(queryset=Options.objects.none())

    return render(request, 'question/create_options.html', {'formset': formset, 'question': question})


def edit_options(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test  # Assuming Test has a ForeignKey to Question

    if request.method == 'POST':
        formset = CreateOptionFormSet(request.POST, queryset=Options.objects.filter(question_id=question_id))
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.question = question  # Assign the question directly
                instance.save()
            formset.save_m2m()  # Save many-to-many relationships
            return redirect('create_question', test_id=test.id)
    else:
        formset = CreateOptionFormSet(queryset=Options.objects.filter(question_id=question_id))

    return render(request, 'question/edit_options.html', {'formset': formset, 'question': question})


def search(request):
    query = request.GET.get('query')
    if query:
        result_lessons = Lessons.objects.filter(
            Q(title__icontains=query) | Q(creator__username__icontains=query)
        )
        result_tests = Test.objects.filter(
            Q(name__icontains=query) | Q(creator__username__icontains=query)
        )
    else:
        result_lessons = []
        result_tests = []

    return render(request, 'search.html', {
        'query': query,
        'lessons': result_lessons,
        'tests': result_tests,
    })
