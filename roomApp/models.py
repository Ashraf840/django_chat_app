from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_added', ]

    def __str__(self):
        return self.content


class UserOnline(models.Model):
    user = models.ForeignKey(User, related_name='UserConnectionActivity', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='UserConnectionActivity', on_delete=models.CASCADE)
    is_active = models.BooleanField(verbose_name="Online", default=True)
    joined_at = models.DateTimeField(verbose_name="First Joined", auto_now_add=True)  # Updates on creation only
    last_update = models.DateTimeField(verbose_name="Last Activity", auto_now=True)  # Updates on creation & modification
