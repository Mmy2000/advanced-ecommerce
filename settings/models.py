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
    
class Post(models.Model):
    auther = models.ForeignKey(User, related_name="post_auther",verbose_name=_('auther'), on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name=_('title'))
    tags = TaggableManager(_("tags"))
    image = models.ImageField(_("image"),upload_to='post/')
    created_at = models.TimeField( _("created_at"),default=timezone.now)
    description = models.TextField(_("description"),max_length=100000)
    category = models.ForeignKey('Category',related_name='post_category',verbose_name=_('category'),on_delete=models.CASCADE)
    slug = models.SlugField(_("url"),null=True,blank=True)
    views = models.PositiveIntegerField(default=0)

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})
    



class Category(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        verbose_name = "Post Category"
    def __str__(self):
        return self.name