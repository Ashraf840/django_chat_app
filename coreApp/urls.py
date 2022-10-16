from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


class MyLoginView(auth_views.LoginView):
    template_name = 'coreApp/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Login'
        })
        return context


urlpatterns = [
    path('', views.frontPage, name='frontPage'),
    path('signup/', views.signup, name='signup'),
    # path('login/', auth_views.LoginView.as_view(template_name='coreApp/login.html'), name='login'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', views.userLogout, name='logout'),
]
