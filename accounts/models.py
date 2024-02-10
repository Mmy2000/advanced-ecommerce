from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify 
from django.utils import timezone
# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError('user must have an email address')
        if not username:
            raise ValueError('user must have an username')
        
        user = self.model(
            email = self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name,last_name,username,email,password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            last_name=last_name,
            first_name=first_name,
        )

        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)
        return user
    
    