from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, first_name, last_name, age, gender, password):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name, last_name, age, gender):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    created_on = models.DateTimeField(verbose_name='Sign Up Date', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'gender', 'age']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin


class DailyCommute(models.Model):
    journey_title = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    source_long = models.DecimalField(max_digits=9, decimal_places=6)
    source_lat = models.DecimalField(max_digits=9, decimal_places=6)
    destination_long = models.DecimalField(max_digits=9, decimal_places=6)
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6)
    start_time = models.DateTimeField(verbose_name=' Journey Start Time')
    created_on = models.DateTimeField(verbose_name='Creation Date', auto_now_add=True)

    REQUIRED_FIELDS = ['journey_title', 'source_long', 'source_lat', 'destination_lat', 'destination_long', 'start_time']

    def __str__(self):
        return self.journey_title
