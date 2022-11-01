from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
User = get_user_model()
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user = instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.user_profile.save()


@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created and instance.email:
        send_mail('Welcome to Delevery SYstem', f"Hello {instance.username}! Welcome to Best deleviry System", settings.DEFAULT_FROM_EMAIL, [instance.email])