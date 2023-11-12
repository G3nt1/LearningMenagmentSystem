from django.shortcuts import render, redirect, get_object_or_404
from lms.forms import CreateTestForm, CreateQuestionForm, CreateOptionFormSet, CreateOptionForm
from lms.models import Test, Question, Options
from django.forms import modelformset_factory


# test /.................
def tests(request):
    test = Test.objects.all()
    return render(request, 'test/show_test.html', {'tests': test})


def create_test(request):
    if request.method == 'POST':
        form = CreateTestForm(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.creator = request.user
            test.save()
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
    questions = Question.objects.filter(test__name=test.name)
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
        return render(request, 'question/create_question.html', {"form": form, "test": test, "questions": questions})


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


# ...  Options

def create_options(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    test = question.test

    if request.method == 'POST':
        formset = CreateOptionFormSet(request.POST)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.question_id = question_id
                instance.save()
            return redirect('create_question', test_id=test.id)
    else:
        formset = CreateOptionFormSet(initial=[{'question_id': question_id}])

    return render(request, 'question/create_options.html', {'formset': formset, 'question': question, 'test': test})
