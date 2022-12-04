from django.shortcuts import render, redirect
from .forms import UserLoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from .decorators import stop_authenticated_users
from .emailVerification import emailVerification




def check_email_verification(request):
    context = {
        'title': 'Email Verification',
    }
    return render(request, 'accountApp/reg_process_templates/check_email_verification.html', context)




@stop_authenticated_users
def signup(request):
    context = {
        'title': 'Signup',
    }
    if request.method == "POST":
        form = SignupForm(request.POST)
        # context['form'] = form    # NOT NECESSARY
        if form.is_valid():
            # First Check if the mail is sent without an error; TRY TO USE A TRY-CATCH BLOCK
            user = form.save()

            req_dict_domain = request.headers['Host']

            # send test mail
            # emailVerification(req_dict_domain, user_email=form.cleaned_data['email'], user=user)
            emailVerification(req_dict_domain=req_dict_domain, user=user)
            return redirect('accountApp:check_email_verification')
            # login(request, user)
            # return redirect('coreApp:home')
        # [OPTIONAL]: NOT REQUIRED CURRENTLY; SINCE SIGNUP FORM IS CONSTRUCTED INTO HTML
        # else:
        #     print("No POST method is called!")
        #     form = SignupForm()
        #     context['form'] = form

    return render(request, 'accountApp/signup.html', context)


def userLogout(request):
    logout(request)
    return redirect('accountApp:login')


@stop_authenticated_users
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
