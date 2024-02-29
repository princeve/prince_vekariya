from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe


# Create your models here.
class Level(models.Model):
    name = models.CharField(max_length=100, default="", blank=True)

    class Meta:
        verbose_name_plural = '2. Level'


    def __str__(self):
        return self.name

class Category(models.Model):
    slug = models.CharField(max_length=100, null=False, unique=True)
    category_name = models.CharField(max_length=100, default="",null=True)
    icon = models.CharField(max_length=100, default="",null=True)
    status = models.BooleanField(default="", help_text="0=default, 1=Hidden")
    trending = models.BooleanField(default="", help_text="0=default, 1=Hidden")
    image = models.ImageField(upload_to='Students/Category_image', blank=True)
    create_at = models.DateTimeField(auto_now_add=True,)
    update_at = models.DateTimeField(auto_now=True)

    def image_tag(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    class Meta:
        verbose_name_plural = '1. Category'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


    def __str__(self):
            return self.category_name  # __str__ method elaborated later in



class Language(models.Model):
    language = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return self.language

    class Meta:
        verbose_name_plural = '3.Language'


