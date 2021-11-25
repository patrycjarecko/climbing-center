from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

class Role (models.Model):
    name = models.CharField(max_length=30)

class Client (models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    card_number = models.CharField(primary_key=True, max_length=6, validators=[RegexValidator(r'^\d{1,10}$')])
    password = models.CharField(max_length=30)
    birthday = models.DateField
    email = models.EmailField()


class Instructor (models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=15)
    username = models.CharField(max_length=15)
    role = models.ManyToManyField(Role)


class Interval (models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()


class SectionType (models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    price_once_a_week = models.IntegerField(validators=[MinValueValidator(1)])
    max_count = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])


class Section (models.Model):
    week_day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    interval = models.ForeignKey(Interval, on_delete=models.CASCADE)
    section_type = models.ForeignKey(SectionType, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)


class PassType (models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(validators=[MinValueValidator(1)])
    max_entry_count = models.IntegerField(validators=[MinValueValidator(1)])
    expiration_date = models.IntegerField(validators=[MinValueValidator(1)])


class Pass (models.Model):
    month = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    pass_type = models.ForeignKey(PassType, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

class Entrance(models.Model):
    date = models.DateField()
    pass_model = models.ForeignKey(Pass, on_delete=models.CASCADE)

