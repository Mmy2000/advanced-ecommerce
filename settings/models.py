from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.text import slugify 
from django.utils.translation import gettext_lazy as _
from accounts.models import User
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

# Create your models here.
class Contact(models.Model):
    name = models.CharField(_("username"),max_length=250)
    email = models.EmailField(_("email"),)
    phone = models.CharField(_("phone"),max_length=11)
    message = models.TextField(_("message"),max_length=3000)

    class Meta:
        verbose_name = _("Contacts")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.email
    
class Settings(TranslatableModel):
    translations = TranslatedFields(
        site_name = models.CharField(_("site_name"), max_length=50),
        address = models.CharField(_("address"), max_length=50),
        get_in_touch = models.TextField(_("get_in_touch"),max_length=1000),
        phone = models.CharField(_("phone"), max_length=30),
        description = models.TextField(_("description"),max_length=1000)
    )
    
    logo = models.ImageField(_("logo"), upload_to='setting/')
    email = models.EmailField(_("email"), max_length=254)
    fb_link = models.URLField(_("fb_link"), max_length=200)
    snap_link = models.URLField(_("snapchat_link"), max_length=200)
    instagram_link = models.URLField(_("instagram_link"), max_length=200)
    tiktok_link = models.URLField(_("tiktok_link"), max_length=200)
    phone2 = models.CharField(_("phone2"), max_length=30)

    class Meta:
        verbose_name = _("Settings")
        verbose_name_plural = _("Settings")

    def __str__(self):
        return self.site_name
    
class NewsLitter(models.Model):
    email = models.EmailField(_("email"), max_length=254)
    name = models.CharField(_("name"),null=True,blank=True, max_length=50)
    created_at = models.DateTimeField(_("created_at"),default=timezone.now)
    

    class Meta:
        verbose_name = _("NewsLitter")
        verbose_name_plural = _("NewsLitter")

    def __str__(self):
        return self.email
    
class About(TranslatableModel):
    
    image = models.ImageField(_("image"), upload_to='about/')
    translations = TranslatedFields(
        what_we_do = models.TextField(_("what_we_do"), max_length=5000),
        our_mission = models.TextField(_("our_mission"),max_length=5000),
        our_gaols = models.TextField(_("our_gaols"),max_length=5000),
    )

    class Meta:
        verbose_name = _("About")
        verbose_name_plural = _("About")

    def __str__(self):
        return str(self.id)
    
class FAQ(TranslatableModel):
    
    translations = TranslatedFields(
        title = models.CharField(_("title"), max_length=150),
        description = models.TextField(_("description"),max_length=3000)
    )

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")

    def __str__(self):
        return self.title
    
class Images(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_("title"), max_length=150 , help_text=_('this title is display in slider in home page')),
        offer = models.CharField(_("offer"), max_length=250 , null=True , blank=True)
    )
    settings = models.ForeignKey(Settings, related_name='home_image',verbose_name="home_image", on_delete=models.CASCADE)
    
    image = models.ImageField(_("image"), upload_to='homeImages/' , help_text='this image is display in slider in home page')

    class Meta:
        verbose_name = _("Home Images")
        verbose_name_plural = _("Home Images")

    def __str__(self):
        return self.title
    
