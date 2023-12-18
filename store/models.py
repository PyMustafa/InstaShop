from django.db import models
from django.utils.text import slugify

from category.models import Category


# Create your models here.

def product_image_path(instance, filename):
    return f"product/images/{instance.slug}/{filename}"


class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.IntegerField(default=1)
    image = models.ImageField(upload_to=product_image_path, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
