from django.shortcuts import render, redirect, get_object_or_404
from lms.models import Test
from lms.forms import CreateTestForm


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
            return redirect('home')
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

    return render(request, 'test/delete_test.html', {"test":test})




