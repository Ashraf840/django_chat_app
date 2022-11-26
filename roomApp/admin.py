from django.contrib import admin
from .models import *


class UserOnlineAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'room', 'is_active', 'joined_at', 'last_update']
    list_display_links = ['id']
    search_fields = ['is_active', 'joined_at', 'last_update']
    readonly_fields = ['joined_at', 'last_update'] # to view these fields in the "Food" model inside the admin-panel, it's required to explicitly mention these fields as readonly fields, oetherwise they won't be visible.
    list_filter = ['is_active', 'joined_at', 'last_update']
    list_per_page = 15
    ordering = ['id']


class UserConnectedChannelsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_online', 'user_online_obj_char', 'channel_value']
    list_display_links = ['id']
    search_fields = ['id', 'user_online_obj_char', 'channel_value']
    list_per_page = 15
    ordering = ['id']


admin.site.register(Room)
admin.site.register(Message)
admin.site.register(UserOnline, UserOnlineAdmin)
admin.site.register(UserConnectedChannels, UserConnectedChannelsAdmin)
