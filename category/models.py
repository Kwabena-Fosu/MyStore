from django.db import models
from PIL import Image
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    category_slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='photos/categories')

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.category_slug])

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 200:
            output_size = (400, 200)

            img.thumbnail(output_size)

            try:
                img.save(self.image.path)
            except IOError:
                # Handle error when the image cannot be saved
                print('Unable to save image')
    