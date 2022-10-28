from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    class GENDER(models.TextChoices):
        MALE = "MALE", 'MALE'
        FEMALE = "FEMALE", 'FEMALE'
        OTHERS = "OTHERS", 'OTHERS'

    age = models.PositiveIntegerField(blank = True, null=True)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER.choices, blank=True, null=True)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile/image/', default = 'profile.jpg', null=True, blank=True)
    bio = models.TextField(max_length=5000)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phoneNumber = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username


