from django.urls import path
from . import views

app_name = 'accountApp'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.userLogin, name='login'),
    path('logout/', views.userLogout, name='logout'),
]