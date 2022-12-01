from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views
from accountApp import views as authViews

app_name = 'coreApp'

urlpatterns = [
    path('', views.home, name='home'),
]
