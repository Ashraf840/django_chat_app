from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


@login_required
def roomsList(request):
    rooms = Room.objects.all()
    # rooms = [i for i in range(9)]
    context = {
        'title': 'Rooms',
        'rooms': rooms,
    }
    return render(request, 'roomApp/roomList.html', context)


@login_required
def roomDetail(request, slug):
    room = Room.objects.get(slug=slug)
    people = [i for i in range(5)]
    sample = [i for i in range(15)]
    context = {
        'title': room.name,
        'room': room,
        'people': people,
        'sample': sample,
    }
    return render(request, 'roomApp/roomDetail.html', context)


