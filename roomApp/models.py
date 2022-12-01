from django.db import models
# from django.contrib.auth.models import User
from accountApp.models import User


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

    class Meta:
        verbose_name_plural = 'Users Online'


class UserConnectedChannels(models.Model):
    user_online = models.ForeignKey(UserOnline, related_name='UserConnectionChannels', on_delete=models.CASCADE)
    user_online_obj_char = models.CharField(max_length=255, blank=True, null=True)
    channel_value = models.CharField(verbose_name='Channel Name', max_length=74, help_text='Every channel name consists of a specific 74 chars')

    class Meta:
        verbose_name_plural = 'User Channel Connections'

    def save(self, *args, **kwargs):
        if self.user_online_obj_char is None:
            self.user_online_obj_char = self.user_online.room.slug + "-" + self.user_online.user.username
        super(UserConnectedChannels, self).save(*args, **kwargs)
