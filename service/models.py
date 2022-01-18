from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings

class Role (models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"

class Client (models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    card_number = models.CharField(primary_key=True, max_length=6)
    birthday = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class InstructorManager(BaseUserManager):
    def create_user(self, username, password=None, first_name='', last_name='', email='', role=None):

        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

class Instructor (AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
    username = models.EmailField(unique=True)
    role = models.ManyToManyField(Role)
    objects = InstructorManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Interval (models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


class SectionType (models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    price_once_a_week = models.IntegerField(validators=[MinValueValidator(1)])
    max_count = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Section (models.Model):
    week_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Typ:{self.section_type} interval: {self.interval}"


class PassType (models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    max_entry_count = models.IntegerField(validators=[MinValueValidator(1)])
    expiration_date = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.name}"


class Pass (models.Model):
    month = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE, blank=True, null=True)
    pass_type = models.ForeignKey(PassType, on_delete=models.CASCADE, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID: {self.id} Client: {self.client}"

class Entrance(models.Model):
    date = models.DateField()
    pass_model = models.ForeignKey(Pass, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} - {self.pass_model}"
