from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.text import slugify 
from accounts.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
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
        return reverse("post_detail", kwargs={"pk": self.pk})
    

class Category(models.Model):
    name = models.CharField(max_length=60)
    class Meta:
        verbose_name = "Post Category"
    def __str__(self):
        return self.name