from django.shortcuts import render, redirect
from .forms import UserLoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from .decorators import stop_authenticated_users
from .emailVerification import emailVerification
from django.contrib import messages


# TODO: Add flash msg in auth system.
# TODO: Make the auth system under class-based views.
# TODO: Make password-reset using email-verification feature.


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
            # emailVerification(req_dict_domain=req_dict_domain, user=user)
            # return redirect('accountApp:check_email_verification')
            login(request, user)
            return redirect('coreApp:home')
        # [OPTIONAL]: NOT REQUIRED CURRENTLY; SINCE SIGNUP FORM IS CONSTRUCTED INTO HTML
        else:
            #     print("No POST method is called!")
            #     form = SignupForm()
            context['form'] = form

    return render(request, 'accountApp/signup.html', context)


def userLogout(request):
    logout(request)
    return redirect('accountApp:login')


@stop_authenticated_users
def userLogin(request):
    context = {'title': 'User Login', 'form': UserLoginForm()}

    # [GET req] Render the form while the page loads
    # form = UserLoginForm()

    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # NB: instead of request.POST['xyz']; it's best practice to use form.cleaned_data
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('coreApp:home')
            else:
                # "django.contrib.messages" lib contains auth-error msg
                messages.info(request, "Invalid Credentials!")
        else:
            # print('Form error:', form.errors)
            # print('Form email-field error:', form.errors.get('email'))
            # print('Form password-field error:', form.errors.get('password'))
            # "form.errors" passed to frontend using context-dict; form-field-specific-errors
            context['form'] = form  # pass the form.errors into HTML

    return render(request, 'accountApp/login.html', context)
