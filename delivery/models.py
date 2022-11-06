from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import gettext as _
import uuid
from django.contrib.auth import get_user_model
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=300)
    slug = AutoSlugField(_('slug'), max_length=50, unique=True, populate_from=('name'))

    def __str__(self):
        return self.name

class Jobs(models.Model):
    class SIZES(models.TextChoices):
        SMALL_SIZE = "small", 'Small'
        MEDIUM_SIZE = "medium", 'Medium'
        LARGE_SIZE = "large", 'Large'
    
    class STATUS(models.TextChoices):
        CREATING_STATUS = 'creating', 'Creating'
        PROCESSING_STATUS = 'processing', 'Processing'
        PICKING_STATUS = 'picking','Picking'
        DELIVERING_STATUS = 'delivering',' Delivering'
        COMPLETED_STATUS = 'completed', 'Completed'
        CANCELED_STATUS = 'canceled', 'Canceled'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=300)
    bio = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    size = models.CharField(max_length=255, choices=SIZES.choices, default=SIZES.MEDIUM_SIZE)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='jobs/photos/')
    status = models.CharField(max_length=30, choices=STATUS.choices, default=STATUS.CREATING_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)