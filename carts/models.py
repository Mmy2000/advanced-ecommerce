from django.db import models
from django.utils import timezone
from products.models import Coupon

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField( max_length=50 , null=True, blank=True)
    date_added = models.DateField(default=timezone.now)


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey("accounts.User",null=True, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    variations = models.ManyToManyField("products.Variation",blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE ,blank=True ,  null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
# Create your models here.
