from django.db import models
from accounts.models import User

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField( max_length=100)
    payment_method = models.CharField( max_length=100)
    payment_paid = models.CharField( max_length=100)
    status = models.CharField( max_length=100)
    created_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.payment_id
    

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Accepted','Accepted'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    payment = models.ForeignKey(Payment,  on_delete=models.SET_NULL ,blank=True , null=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=50,blank=True)
    email = models.EmailField( max_length=254)
    address_line_1 = models.CharField( max_length=50)
    address_line_2 = models.CharField( max_length=50 , blank=True)
    country = models.CharField( max_length=50 )
    state = models.CharField( max_length=50 )
    city = models.CharField( max_length=50 )
    order_note = models.CharField( max_length=1000 , blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(choices=STATUS,default='New' , max_length=15)
    ip = models.CharField(max_length=50  ,blank=True)
    is_orderd = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'

    def __str__(self):
        return self.first_name
    
class OrderProduct(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL ,blank=True , null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    variations = models.ManyToManyField("products.Variation",blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name