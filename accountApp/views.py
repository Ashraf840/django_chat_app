from django.shortcuts import render, redirect
from .forms import UserLoginForm, SignupForm
from django.contrib.auth import authenticate, login, logout
from .decorators import stop_authenticated_users
from .emailVerification import emailVerification
from django.contrib import messages


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
            # emailVerification(req_dict_domain, user_email=form.cleaned_data['email'], user=user)      # NOT USING; REDUNDANT UNTIL USING THE "form.cleaned_data['email']"
            emailVerification(req_dict_domain=req_dict_domain, user=user)
            return redirect('accountApp:check_email_verification')
            # login(request, user)
            # return redirect('coreApp:home')
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

            # if form.errors.get('email') is not None:
            #     print('Form email-field error:', form.errors.get('email'))
            # if form.errors.get('password') is not None:
            #     print('Form password-field error:', form.errors.get('password'))

            # print('Form fields (email-error):', dir(form.fields.get('email')))
            # print('Form fields (email-error):', form.fields.get('email').error_messages)
            # print('Form fields (password-error):', form.fields.get('password').error_messages)
            # print('Form fields (password-error):', form.fields.get('password'))

            # "form.errors" passed to frontend using context-dict; form-field-specific-errors
            context['form'] = form  # pass the form.errors into HTML

    return render(request, 'accountApp/login.html', context)


from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


def check_email_pass_reset(request):
    context = {
        'title': 'Password Reset',
    }
    return render(request, 'accountApp/password_reset_templates/check_email_pass_reset.html', context)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accountApp/password_reset_templates/password_reset.html'
    email_template_name = 'accountApp/password_reset_templates/email_templates/pass_reset.txt'
    html_email_template_name = 'accountApp/password_reset_templates/email_templates/pass_reset.html'
    subject_template_name = 'accountApp/password_reset_templates/email_templates/pass_reset_email_subj.txt'
    # success_message = "We've emailed you instructions for setting your password, " \
    #                   "if an account exists with the email you entered. You should receive them shortly." \
    #                   " If you don't receive an email, " \
    #                   "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('accountApp:check_email_pass_reset')
