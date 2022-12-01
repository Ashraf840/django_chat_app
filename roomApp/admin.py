from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = ['name']
    search_fields = ['name', 'slug']
    list_per_page = 15
    ordering = ['-id']
    # Autopopulate the slug-field of chatRoom-name, while writing teh room-name
    prepopulated_fields = {
        "slug": ("name",)
    }


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'room', 'user', 'content', 'date_added']
    list_display_links = ['id']
    search_fields = ['content', 'date_added']
    readonly_fields = ['date_added']
    list_filter = ['date_added']
    list_per_page = 15
    ordering = ['-date_added']


class UserOnlineAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'is_active', 'joined_at', 'last_update']
    list_display_links = ['id']
    search_fields = ['is_active', 'joined_at', 'last_update']
    readonly_fields = ['joined_at', 'last_update']
    list_filter = ['is_active', 'joined_at', 'last_update']
    list_per_page = 15
    ordering = ['id']


class UserConnectedChannelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_online', 'user_online_obj_char', 'channel_value']
    list_display_links = ['id']
    search_fields = ['id', 'user_online_obj_char', 'channel_value']
    list_per_page = 15
    ordering = ['id']


admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(UserOnline, UserOnlineAdmin)
admin.site.register(UserConnectedChannels, UserConnectedChannelsAdmin)
