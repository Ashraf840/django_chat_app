from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'username', 'first_name', 'last_name', 'gender', 'phone', 'country', 'date_joined', 'last_login', 'last_update', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
    list_display_links = ['email']
    search_fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone', 'country']
    readonly_fields = ['password', 'date_joined', 'last_login', 'last_update'] # to view these fields in the "User List" model inside the admin-panel, it's required to mention explicitly these fields as readonly fields to views the fields related to date.
    # Customize the user-detail page
    fieldsets = [
        ('User Information', {
            'fields': ('email', 'password', 'username', ('first_name', 'last_name'), 'gender', 'phone', 'country', 'profile_pic'),
            'classes': ('wide',),
        }),
        ('Registration & Activity', {
            'fields': ('date_joined', 'last_login', 'last_update')
        }),
        ('Roles', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')
        }),
        ('Groups', {
            'fields': ('groups',),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('user_permissions',),
            'classes': ('collapse',)
        }),
    ]
    list_filter = ['gender', 'date_joined', 'last_login', 'last_update', 'is_active', 'is_staff', 'is_admin', 'is_superuser']
    list_per_page = 15
    ordering = ['-date_joined']
    # Customize the user-creation page
    add_fieldsets = [
        ('User Information', {
            'fields': ('email', 'username', ('first_name', 'last_name'),
                       'gender', 'phone', 'country', 'profile_pic', 'password1', 'password2'),
            'classes': ('wide',),
        })
    ]


admin.site.register(User, UserAdmin)
