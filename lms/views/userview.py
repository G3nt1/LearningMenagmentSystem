from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from lms.forms import CreateUserForm, LoginUserForm, ProfileUserForm


def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        profile = ProfileUserForm(request.POST, request.FILES)

        if form.is_valid() and form.is_valid():
            user = form.save(commit=False)
            user.username = form.cleaned_data['email']
            user.save()

            profile = profile.save(commit=False)
            profile.username = user
            profile.save()
            return redirect('login')
    else:
        form = CreateUserForm()
        profile = ProfileUserForm()
    context = {'form': form, 'profile': profile}

    return render(request, 'users/register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = LoginUserForm()
    return render(request, 'users/login.html', {'form': form})


def userLogout(request):
    logout(request)
    return redirect('login')
