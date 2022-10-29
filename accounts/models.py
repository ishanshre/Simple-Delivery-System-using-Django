from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor_uploader.fields import RichTextUploadingField

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
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    avatar = models.ImageField(upload_to='profile/image/', default = 'profile.jpg', null=True, blank=True)
    bio = RichTextUploadingField(max_length=10000)
    country = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phoneNumber = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.user.username


