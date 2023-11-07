from django.shortcuts import render, redirect, get_object_or_404
from lms.models import Test
from lms.forms import CreateTestForm


def tests(request):
    tests = Test.objects.all()
    return render(request, 'test/show_test.html', {'tests': tests})


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
