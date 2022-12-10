from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from . import emailVerification as ev
from django.urls import reverse_lazy

app_name = 'accountApp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    # Email Verification
    path('email-verification/', views.check_email_verification, name='check_email_verification'),
    path('activate/<uidb64>/<token>/', ev.VerificationView.as_view(), name='activate'),
    # the name 'activate' is used in the 'link' variable of 'activate_url'
    # Password Reset
    path('email-password-reset/', views.check_email_pass_reset, name='check_email_pass_reset'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accountApp/password_reset_templates/password_reset_confirm.html',
             success_url=reverse_lazy("accountApp:password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accountApp/password_reset_templates/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]


"""
NB: "password_reset_confirm" was unable to find the next URL to proceed after succession. 
Thus it requires to define the 'success_url' explicitly.
Idea got from: https://stackoverflow.com/a/59457967
"""