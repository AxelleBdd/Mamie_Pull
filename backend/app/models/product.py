from django.db import models
from models.category import Category

class Product (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, #prevent deleting category if it's used by at least one product
        related_name="products")
    #image = models.ImageField(upload_to="products/")

    def __str__(self):
        return self.title