from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, username, first_name, last_name, age, gender, password, pref_mode_travel, pref_gender, country, phone_number, rating=None, total_rating_count=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            rating=rating,
            total_rating_count=total_rating_count,
            pref_gender=pref_gender,
            pref_mode_travel=pref_mode_travel,
            country=country,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, first_name, last_name, age, gender, pref_mode_travel, pref_gender, country, phone_number):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
            first_name=first_name,
            last_name=last_name,
            age=age,
            gender=gender,
            pref_gender=pref_gender,
            pref_mode_travel=pref_mode_travel,
            country=country,
            phone_number=phone_number
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
    country = models.CharField(null=True, max_length=30)
    phone_number = models.BigIntegerField(null=True)

    pref_gender = models.IntegerField()
    pref_mode_travel = models.IntegerField()
    rating = models.FloatField(default=0, null=True)
    total_rating_count = models.IntegerField(default=0, null=True)

    created_on = models.DateTimeField(verbose_name='Sign Up Date', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Last Login', auto_now=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'gender', 'age', 'pref_gender', 'pref_mode_travel', 'country', 'phone_number']
    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin
