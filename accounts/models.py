from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.text import slugify 
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    first_name      = models.CharField(_("first_name"),max_length=50)
    last_name       = models.CharField(_("last_name"),max_length=50)
    username        = models.CharField(_("username"),max_length=50, unique=True)
    email           = models.EmailField(_("email"),max_length=100, unique=True)
    phone_number    = models.CharField(_("phone_number"),max_length=50)
    
    # required
    date_joined     = models.DateTimeField(_("date_joined"),auto_now_add=True)
    last_login      = models.DateTimeField(_("last_login"),auto_now_add=True)
    is_admin        = models.BooleanField(_("is_admin"),default=False)
    is_staff        = models.BooleanField(_("is_staff"),default=False)
    is_active        = models.BooleanField(_("is_active"),default=False)
    is_superadmin        = models.BooleanField(_("is_superadmin"),default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = _("Users")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
class Profile(models.Model):
    user = models.OneToOneField(User,verbose_name=_("user profile"),on_delete=models.CASCADE)
    address = models.CharField(_("address"),max_length=50,blank=True , null=True)
    image = models.ImageField(_("image"),upload_to='users_images/',blank=True , null=True)
    about = models.TextField(_("about"),max_length=4000 , blank=True , null=True)
    country = models.CharField(_("country"),max_length=50 ,blank=True, null=True)
    company = models.CharField(_("company"),max_length=100 ,blank=True, null=True)
    address_line_1 = models.CharField(_("address_line_1"), max_length=50 , blank=True , null=True)
    address_line_2 = models.CharField(_("address_line_2"), max_length=50 , blank=True , null=True)
    headline = models.CharField(_("headline"),max_length=50 , blank=True, null=True)
    city = models.CharField(_("city"),max_length=50 ,blank=True, null=True)


    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    def full_address(self):
        return f"{self.country} | {self.city} | {self.address_line_1} {self.address_line_2}"

    class Meta:
        verbose_name = _("Profiles")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)