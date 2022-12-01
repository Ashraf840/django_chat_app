from django.contrib.auth.models import BaseUserManager


# Manager class to manage user-model (Super & Regular User)
class UserManager(BaseUserManager):
    # Create regular users
    def create_user(self, email, username, password=None):
        # Check basic validations for the required fields of "CustomUser" class
        if not email:
            raise ValueError('Email is required!')
        if not username:
            raise ValueError('Username is required!')

        #  Create a user model
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Create superusers
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
