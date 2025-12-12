from django.db import models
from models.category import Category

class Product (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category_id = models.CharField(max_length=100)
    #image = models.ImageField(upload_to="products/", blank=True, null=True)

    categories = models.ManyToManyField(Category, related_name="products")

    def __str__(self):
        return self.title