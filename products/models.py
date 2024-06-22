from django.db import models
from django.utils import timezone
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from accounts.models import  User
from django.db.models import Avg , Count
from taggit.managers import TaggableManager
from django.core.validators import MaxValueValidator , MinValueValidator
# Create your models here.
class Product(models.Model):
    name = models.CharField(unique=True, max_length=50)
    image = models.ImageField(upload_to='product/')
    stock = models.IntegerField(default=1)
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    created_at = models.DateTimeField( default=timezone.now)
    slug = models.SlugField(null=True,blank=True , unique=True)
    views = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    tags = TaggableManager()
    subcategory = models.ForeignKey("Subcategory",verbose_name='Category',related_name='product_subcategory',null=True,blank=True, on_delete=models.CASCADE)
    like = models.ManyToManyField(User , blank=True,related_name='product_favourite')


    class Meta:
        ordering = ["name"]

    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.name)
        if self.stock == 0:
            self.is_available = False
        else :
            self.is_available = True

        super(Product,self).save(*args,**kwargs)
    
    def avr_review(self):
        reviews = ReviewRating.objects.filter(product=self , status=True).aggregate(average=Avg('rating'))
        avg =0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg
    
    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self , status=True).aggregate(count=Count('rating'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


    def get_absolute_url(self):
        return reverse("product_detail", args=[self.subcategory.id,self.slug])
    
    def __str__(self):
        return self.name


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_category='color',is_active=True)
    
    def sizes(self):
        return super(VariationManager,self).filter(variation_category='size',is_active=True)

variation_category_choice=(
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Product,related_name='product_variation',  on_delete=models.CASCADE)
    variation_category = models.CharField( max_length=200 , choices=variation_category_choice)
    variation_value = models.CharField( max_length=200 )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(  auto_now_add=True)
    objects = VariationManager()


    def __str__(self):
        return self.variation_value

class ProductImages(models.Model):
    product = models.ForeignKey(Product,related_name='product_image',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='productimages/')

    def __str__(self):
        return str(self.product)



class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(null=True,blank=True,upload_to='category-image/')

    def get_url(self):
        return reverse('product_by_subcategory',args=[self.id])
    
    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    

    

    
class ReviewRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='reviewrating', on_delete=models.CASCADE)
    subject = models.CharField(max_length=500 , blank=True)
    review = models.TextField(max_length=500 , blank=True)
    rating = models.FloatField()
    ip = models.CharField( max_length=50 , blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField( auto_now=True)

    def __str__(self):
        return self.subject
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)])
    valid_from = models.DateField(default=timezone.now)
    valid_to = models.DateField(default=timezone.now)
    is_expired = models.BooleanField(default=False)

    def __str__(self):
        return self.code
    