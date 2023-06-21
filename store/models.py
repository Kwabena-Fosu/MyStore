from django.db import models
from category.models import Category
from accounts.models import Account
from django.urls import reverse
import os
from PIL import Image


class Product(models.Model):
    product_name = models.CharField(unique=True, max_length=200)
    product_slug = models.SlugField(unique=True, max_length=200)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name
    
    def get_url(self):
         return reverse('product_detail', args=[self.category.category_slug, self.product_slug])
    
    
    def save(self, *args, **kwargs):
        # Get the original image path before saving
        try:
            product = Product.objects.get(pk=self.pk)
            original_image_path = product.image.path
        except Product.DoesNotExist:
            original_image_path = None
        
        # Get the current image file extension
        image_extension = os.path.splitext(self.image.name)[1]
        
        # Rename the image file to the product name with dynamic extension
        image_name = f"{self.product_name}{image_extension}"
        image_path = os.path.join('', image_name)

        # Assign the new image path to the image field
        self.image.name = image_path
        
        super().save(*args, **kwargs)

        # Delete the original image if it exists
        if original_image_path and original_image_path != self.image.path and os.path.exists(original_image_path):
            os.remove(original_image_path)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (500, 500)

            # Crop the image to the center if it's not square
            if img.width != img.height:
                size = min(img.width, img.height)
                x_center = img.width / 2
                y_center = img.height / 2
                crop_size = (
                    x_center - size / 2,
                    y_center - size / 2,
                    x_center + size / 2,
                    y_center + size / 2,
                )
                img = img.crop(crop_size)

            img.thumbnail(output_size)

            try:
                img.save(self.image.path)
            except IOError:
                # Handle error when the image cannot be saved
                print('Unable to save image')


class Testimonial(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    message = models.TextField(max_length=500, blank=False)
    image = models.ImageField(default='pro.png', upload_to='photos/testimonials')

    def __str__(self):
        return self.author.first_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)

            # Crop the image to the center if it's not square
            if img.width != img.height:
                size = min(img.width, img.height)
                x_center = img.width / 2
                y_center = img.height / 2
                crop_size = (
                    x_center - size / 2,
                    y_center - size / 2,
                    x_center + size / 2,
                    y_center + size / 2,
                )
                img = img.crop(crop_size)

            img.thumbnail(output_size)

            try:
                img.save(self.image.path)
            except IOError:
                # Handle error when the image cannot be saved
                print('Unable to save image')