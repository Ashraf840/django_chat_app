from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignupForm

def frontPage(request):
    context = {
        'title': 'Welcome'
    }
    return render(request, 'coreApp/frontPage.html', context)


def signup(request):
    context = {
        'title': 'Signup',
    }
    if request.method == "POST":
        form = SignupForm(request.POST)
        context['form'] = form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('frontPage')
        else:
            form = SignupForm()
            context['form'] = form

    return render(request, 'coreApp/signup.html', context)


def userLogout(request):
    logout(request)
    return redirect('login')

