from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, # db column can contain null
        blank=True, # not required in forms
        related_name="categories"
        )
    
    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name
