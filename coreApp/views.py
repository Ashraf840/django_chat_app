from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    context = {
        'title': 'Welcome'
    }
    return render(request, 'coreApp/home.html', context)

