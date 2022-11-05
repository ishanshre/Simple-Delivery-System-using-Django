# Generated by Django 4.1.1 on 2022-11-04 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile_is_phonenumber_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='stripe_card_last4',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='profile',
            name='stripe_payment_method_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]