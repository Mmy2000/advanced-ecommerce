from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    message = models.TextField(max_length=3000)

    def __str__(self):
        return self.email