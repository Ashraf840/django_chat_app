from django.shortcuts import render, redirect
from .forms import UserLoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout


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
            return redirect('coreApp:home')
        else:
            form = SignupForm()
            context['form'] = form

    return render(request, 'accountApp/signup.html', context)


def userLogout(request):
    logout(request)
    return redirect('accountApp:login')


def userLogin(request):
    context = {
        'title': 'User Login',
    }

    # [GET req] Render the form while the page loads
    form = UserLoginForm()
    context['loginForm'] = UserLoginForm()

    if request.POST:
        form = UserLoginForm(request.POST)

        email = request.POST['email']
        password = request.POST['password']

        if form.is_valid():
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('coreApp:home')

    return render(request, 'accountApp/login.html', context)
