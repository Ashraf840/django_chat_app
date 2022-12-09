import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .utils import token_generator
from django.views import View
from .models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.http.response import HttpResponse


# Multi-threading; Email will be sent faster & the user will not feel like waiting to be redirected to the login page
class EmailThread(threading.Thread):
    def __init__(self, msg):
        self.email = msg
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


# def emailVerification(user_id=None, req_dict_domain=None, user=None, user_email=None, fullName=None):
def emailVerification(user_email=None, *args, **kwargs):
    # print(f'emailVerification() func args: {args}')
    # print(f'emailVerification() func kwargs: {kwargs}')
    # print(f"User ID: {kwargs['user'].pk}")
    # print(f"User Email: {kwargs['user'].email}")
    # print(f"Host: {kwargs['req_dict_domain']}")
    uidb64 = urlsafe_base64_encode(force_bytes(kwargs['user'].pk))
    domain = kwargs['req_dict_domain']

    link = reverse('accountApp:activate', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(kwargs['user'])})

    activate_url = 'http://' + domain + link

    email_subject = 'Activate you account - Teachatty'
    from_email = 'no-reply@teachatty.xyz'
    to_email = kwargs['user'].email

    # Email templates (both text & html); will be rendered then sent
    context = {'username': kwargs['user'].username, 'activate_url': activate_url, }

    text_content = render_to_string(
        'accountApp/accnt_activation_email_template/regular_user/account_activation.txt', context)
    # Color Palette Used: https://colorhunt.co/palette/393e466d9886f2e7d5f7f7f7
    # Email HTML Template: https://bbbootstrap.com/snippets/confirm-account-email-template-17848137
    html_content = render_to_string(
        'accountApp/accnt_activation_email_template/regular_user/account_activation.html', context)

    # Bug Fix: Email was not able to be sent using ZOHO mailing service
    # [Ref]: https://stackoverflow.com/a/49894619
    # msg = EmailMultiAlternatives(email_subject, text_content, from_email, [to_email])
    # msg.attach_alternative(html_content, "text/html")
    msg = send_mail(email_subject, text_content, from_email, [to_email], html_message=html_content)
    EmailThread(msg).start()


# Redirection link to the login page after user-account activation
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # check_token(): Check that an account activation token is correct for a given user.
            # It simply checks if the token is already been used or not.
            # [Further Task]: Allow user to request for another email-verification-token to complete the activation process.
            if not token_generator.check_token(user, token):
                messages.warning(request, 'Your token is expired! Or, there are some other issues!')
                return redirect('accountApp:login')

            if user.is_active:
                messages.warning(request, 'Your account is already activated!')
                return redirect('accountApp:login')
            else:
                user.is_active = True
                user.save()
                messages.success(request, 'Your account is activated!')
                return redirect('accountApp:login')
        except User.DoesNotExist as e:
            return HttpResponse('User is not found!')

