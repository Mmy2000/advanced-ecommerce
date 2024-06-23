from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.urls import reverse

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=11)
    message = models.TextField(max_length=3000)

    class Meta:
        verbose_name = ("Contacts")
        verbose_name_plural = ("Contacts")

    def __str__(self):
        return self.email
    
class Settings(models.Model):
    site_name = models.CharField( max_length=50)
    logo = models.ImageField( upload_to='setting/')
    phone = models.CharField( max_length=30)
    email = models.EmailField( max_length=254)
    description = models.TextField(max_length=1000)
    fb_link = models.URLField( max_length=200)
    twitter_link = models.URLField( max_length=200)
    instagram_link = models.URLField( max_length=200)
    address = models.CharField( max_length=50)
    get_in_touch = models.TextField(max_length=1000)

    class Meta:
        verbose_name = ("Settings")
        verbose_name_plural = ("Settings")

    def __str__(self):
        return self.site_name
    
class NewsLitter(models.Model):
    email = models.EmailField( max_length=254)
    name = models.CharField(null=True,blank=True, max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    

    class Meta:
        verbose_name = ("NewsLitter")
        verbose_name_plural = ("NewsLitter")

    def __str__(self):
        return self.email
    
class About(models.Model):
    what_we_do = models.TextField( max_length=5000)
    our_mission = models.TextField(max_length=5000)
    our_gaols = models.TextField(max_length=5000)
    image = models.ImageField( upload_to='about/')

    class Meta:
        verbose_name = ("About")
        verbose_name_plural = ("About")

    def __str__(self):
        return str(self.id)
    
class FAQ(models.Model):
    title = models.CharField( max_length=150)
    description = models.TextField(max_length=3000)

    class Meta:
        verbose_name = ("FAQ")
        verbose_name_plural = ("FAQ")

    def __str__(self):
        return self.title
