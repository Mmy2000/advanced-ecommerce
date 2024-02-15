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
    subcategory = models.ForeignKey("Subcategory",related_name='product_subcategory',null=True,blank=True, on_delete=models.CASCADE)
    PRDBrand = models.ForeignKey('Brand' ,related_name='product_brand', on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("Brand "))


    class Meta:
        ordering = ["name"]

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        super(Product,self).save(*args,**kwargs)


    def get_absolute_url(self):
        return reverse("product_detail", args=[self.slug])
    
    def __str__(self):
        return self.name


class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages/')

    def __str__(self):
        return str(self.product)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True,blank=True,upload_to='category-image/')

    def get_url(self):
        return reverse('product_by_subcategory',args=[self.id])
    
    def __str__(self):
        return self.name
    
class Brand(models.Model):
    BRDName = models.CharField(max_length=40)
    image = models.ImageField(upload_to='product_prand/',blank=True, null=True)
    BRDDesc = models.TextField(blank=True, null=True)
    slug = models.SlugField(null=True,blank=True , unique=True)

    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.BRDName)
        super(Brand,self).save(*args,**kwargs)
    
    def get_url(self):
        return reverse('product_by_brand',args=[self.slug])

    def __str__(self):
        return self.BRDName