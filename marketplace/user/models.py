from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=8, unique=True, blank=True, null=True)

    def fullname(self):
        return self.first_name + " " + self.last_name


class Review(models.Model):
    content = models.TextField(max_length=500, blank=True, null=True)
    rate = models.PositiveIntegerField(default=0, validators=[
        MaxValueValidator(5), MinValueValidator(0)
    ])
    for_view = models.BooleanField(default=False, db_index=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, blank=True)
    user = models.OneToOneField(User, related_name='review', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name;

