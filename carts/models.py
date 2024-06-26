from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(_("cart_id"), max_length=50 , null=True, blank=True)
    date_added = models.DateField(_("date_added"),default=timezone.now)

    class Meta:
        verbose_name = _("Carts")
        verbose_name_plural = ("Carts")


    def __str__(self):
        return self.cart_id
    
class CartItem(models.Model):
    user = models.ForeignKey("accounts.User",null=True,verbose_name=_("user cart"), on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", verbose_name=_("product cart"),on_delete=models.CASCADE)
    variations = models.ManyToManyField("products.Variation",blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,verbose_name=_("cart") ,blank=True ,  null=True)
    quantity = models.IntegerField(_("quantity"))
    is_active = models.BooleanField(_("is_active"),default=True)

    class Meta:
        verbose_name = _("Cart Item")
        verbose_name_plural = ("Cart Item")

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)
# Create your models here.
