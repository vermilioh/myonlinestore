from django.db import models
from django.utils.text import slugify


def unique_slug_generator(model_instance, value, slug_field_name):
    slug_candidate = slugify(value)
    slug_exists = True
    counter = 1
    while slug_exists:
        try:
            model_instance.__class__.objects.get(**{slug_field_name: slug_candidate})
            slug_candidate = f"{slugify(value)}-{counter}"
            counter += 1
        except model_instance.__class__.DoesNotExist:
            slug_exists = False
    return slug_candidate


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug_generator(self, self.name, 'slug')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.category:
            self.image.field.upload_to = f'products/{self.category.name}/%Y/%m/%d'
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/%Y/%m/%d/')

    def __str__(self):
        return f"{self.product.name} - Image {self.pk}"