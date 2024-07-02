from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from django.utils.text import slugify
from accounts.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields


class Post(TranslatableModel):
    
    author = models.ForeignKey(User, related_name="post_author", verbose_name=_('author'),null=True, on_delete=models.CASCADE)
    
    created_at = models.TimeField(_("created_at"), default=timezone.now)
    category = models.ForeignKey('Category', related_name='post_category',null=True, verbose_name=_('category'), on_delete=models.SET_NULL)
    translations = TranslatedFields(
        title = models.CharField(_("title"),default="", max_length=100),
        description = models.TextField(_("description"), max_length=100000,default="")
    )
    slug = models.SlugField(null=True, blank=True)
    views = models.PositiveIntegerField(_("views"),default=0)
    tags = TaggableManager(_("tags"))
    image = models.ImageField(_("image"), upload_to='post/',default="")
    

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.author)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("name"),null=True, max_length=60),
    )
    
    

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    def __str__(self):
        return str(self.safe_translation_getter('name', any_language=True))
