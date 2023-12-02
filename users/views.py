from django.contrib import auth, messages
from django.shortcuts import render, redirect

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if request.user.is_superuser:
                    return redirect('index')
                else:
                    return redirect('profile')
    else:
        form = UserLoginForm()
    context = {
        'title': 'Авторизация | IT News',
        'form': form
    }
    return render(request, 'users/login.html', context=context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'title': 'Регистрация | IT News',
        'form': form
    }
    return render(request, 'users/registration.html', context=context)


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    context = {
        'title': 'Профиль | IT News',
        'form': form
    }
    return render(request, 'users/profile.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('index')
