from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)



"""
<div class="grid grid-cols-9 bg-gray-200 px-6 h-12 my-7 mx-5 rounded-xl">
    <div class="bg-pink-300 flex justify-center items-center">
        <img src="{% static 'img/avatar.png' %}" alt="people avatar" height="40" width="40"
             class="border-solid border-4 border-sky-500 rounded-full">
    </div>
    <div class="bg-green-300 col-span-8">
        <p class="font-semibold">John Doe</p>
        <p>msg: Lorem ipsum dolor sit amet.</p>
    </div>
    <div></div>
    <div class="bg-teal-300 flex items-center">
        <small style="font-size:.7rem">date/time</small>
    </div>
</div>
"""

