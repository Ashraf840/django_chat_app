from django.shortcuts import render
from .models import *
from django.contrib.auth.decorators import login_required


# ---------------------------------- ************** IMPORTANT
# #################
# MAKE CUSTOM DECORATOR;
# IT'S THROWING ERROR WHILE I DELETED ALL THE USERS FROM DJ-ADMIN-PANEL & RELOADED THE ROOM-LIST PAGE,
# THE DECORATOR FUNC ABOVE THE 'roomsList' FUNC IS NOT PERFORMING AS REQUIRED
# #################
# ---------------------------------- ************** IMPORTANT

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
    messages = Message.objects.filter(room=room)[:25]  # fetch the first 25 messages of this room
    people = [i for i in range(1)]  # dummy sample
    # sample = [i for i in range(1)]
    # for m in messages:
    #     print(f"Msg dates: {m.date_added}")
    context = {
        'title': room.name,
        'room': room,
        'messages': messages,
        'people': people,
        # 'sample': sample,
    }
    return render(request, 'roomApp/roomDetail.html', context)


