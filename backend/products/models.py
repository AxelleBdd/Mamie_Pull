from django.conf import settings
from django.db import models

from categories.models import Category


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,  # prevent deleting category if used
        related_name="products",
    )
    image = models.ImageField(upload_to="products/", blank=True, null=True)
    sizes = models.JSONField(
        default=list, blank=True, help_text="List of available sizes"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ["title"]

    def __str__(self):
        return self.title
