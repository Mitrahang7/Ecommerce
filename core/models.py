from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
  name = models.CharField(max_length=20)
  slug = models.SlugField(unique=True, blank=True)


  class Meta:
    verbose_name_plural = 'Categories'

  def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate slug if empty
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

  def __str__(self):
    return self.name
  


class Product(models.Model):
  name = models.CharField(max_length=30)
  slug = models.SlugField(unique=True, blank=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  price = models.PositiveIntegerField()
  image = models.ImageField(upload_to='products')
  description = models.TextField()
  on_sale = models.BooleanField(default=False)
  sale_price = models.PositiveIntegerField(blank=True, null=True)

  def save(self, *args, **kwargs):
        if not self.slug:  # Auto-generate slug if empty
            self.slug = slugify(self.name)
        if not self.on_sale:
            self.sale_price = None  # Reset sale_price if not on sale
        super().save(*args, **kwargs)


  def __str__(self):
    return self.name


class Customer(models.Model):
   user= models.OneToOneField(User, on_delete=models.CASCADE)
   first_name= models.CharField(max_length=20)
   last_name= models.CharField(max_length=20)
   email= models.EmailField()
   phone = models.CharField(max_length=15)
   address= models.CharField(max_length=200, null=True, blank=True)

   def __str__(self):
    return self.email