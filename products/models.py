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
    owner = models.ForeignKey(User, related_name='product_owner',verbose_name=_("product_owner"),default="", on_delete=models.CASCADE)
    name = models.CharField(_("product name"),unique=True, max_length=50)
    image = models.ImageField(_("image"),upload_to='product/')
    stock = models.IntegerField(_("stock"),default=1)
    price = models.IntegerField(_("price"),default=0)
    description = models.TextField(_("description"),max_length=10000)
    created_at = models.DateTimeField(_("created_at"), default=timezone.now)
    slug = models.SlugField(_("slug"),null=True,blank=True , unique=True)
    views = models.PositiveIntegerField(_("views"),default=0)
    is_available = models.BooleanField(_("is_available"),default=True)
    tags = TaggableManager()
    subcategory = models.ForeignKey("Subcategory",verbose_name=_('product Category'),related_name='product_subcategory',null=True,blank=True, on_delete=models.CASCADE)
    like = models.ManyToManyField(User , blank=True,related_name='product_favourite',verbose_name=_('like'))


    class Meta:
        ordering = ["name"]
        verbose_name = _("Products")
        verbose_name_plural = _("Products")

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
    product = models.ForeignKey(Product,related_name='product_image',verbose_name=_('product'),on_delete=models.CASCADE)
    image = models.ImageField(_("product images"),upload_to='productimages/')


    class Meta:
        verbose_name = _("Product Images")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return str(self.product)

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Categories")

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name=_("Category") , blank=True , null=True)
    name = models.CharField(_("subcategory name"),max_length=100)
    image = models.ImageField(_("subcategory image"),null=True,blank=True,upload_to='category-image/')

    def get_url(self):
        return reverse('product_by_subcategory',args=[self.id])
    
    class Meta:
        verbose_name_plural = _("Subcategories")
        verbose_name = _("Subcategories")
        permissions = [
            ('can_translate', 'Can translate using Rosetta'),
        ]

    def __str__(self):
        return self.name
    

    

    
class ReviewRating(models.Model):
    user = models.ForeignKey(User,verbose_name=_('user review'), on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='reviewrating',verbose_name=_('product review'), on_delete=models.CASCADE)
    subject = models.CharField(_("subject"),max_length=500 , blank=True)
    review = models.TextField(_("review"),max_length=500 , blank=True)
    rating = models.FloatField(_("rating"),)
    ip = models.CharField(_("ip"), max_length=50 , blank=True)
    status = models.BooleanField(_("status"),default=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Rating")

    def __str__(self):
        return self.subject
    

    