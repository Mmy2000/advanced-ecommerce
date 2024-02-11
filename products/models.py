from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import  User
from django.db.models import Avg , Count
from taggit.managers import TaggableManager

# Create your models here.
class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    image = models.ImageField(upload_to='product/')
    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    created_at = models.DateTimeField( default=timezone.now)
    slug = models.SlugField(null=True,blank=True , unique=True)
    views = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    tags = TaggableManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
    