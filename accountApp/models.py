from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager   # Manages "Super & Regular Users"
from django.contrib.auth.validators import UnicodeUsernameValidator
from django_countries.fields import CountryField    # install this pip-repo within linux env, update the 'requirements_linux.txt' file by defining this pip-repo, then copy that into local machine using filezilla/winscp

"""
user-fields
-----------
email,username,first_name,last_name,gender,phone,
country,profile_pic,date_joined,last_login,last_update,
is_active,is_staff,is_admin,is_superuser,
"""

username_validator = UnicodeUsernameValidator()

GENDERCHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other'),
]


class User(AbstractBaseUser, PermissionsMixin):
    # User Info
    email = models.EmailField(verbose_name='Email', max_length=60, unique=True)
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
        validators=[username_validator],
        error_messages={
            "unique": "A user with that username already exists.",
        },
    )
    first_name = models.CharField(verbose_name='First Name', max_length=50, blank=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=50, blank=True)
    gender = models.CharField(verbose_name='Gender', max_length=6, choices=GENDERCHOICES, blank=True)
    phone = models.CharField(verbose_name='Primary Contact', max_length=20, blank=True)
    country = CountryField(blank=True)
    profile_pic = models.ImageField(upload_to='profilePicture', blank=True)
    # Registration, Activity
    date_joined = models.DateField(verbose_name='Date Joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name="Last Update", auto_now=True)
    # Extend Roles & Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "User"

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def save(self, *args, **kwargs):
        print(f"profile pic: {self.profile_pic}")
        super(User, self).save(*args, **kwargs)
