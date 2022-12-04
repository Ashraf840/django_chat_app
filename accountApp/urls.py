from django.urls import path
from . import views
from . import emailVerification as ev

app_name = 'accountApp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
    # Email Verification
    path('email-verification/', views.check_email_verification, name='check_email_verification'),
    path('activate/<uidb64>/<token>/', ev.VerificationView.as_view(), name='activate'),      # the name 'activate' is used in the 'link' variable of 'activate_url'
]