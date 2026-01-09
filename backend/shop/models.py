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
    
class Product (models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, 
        on_delete=models.PROTECT, #prevent deleting category if it's used by at least one product
        related_name="products")
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products"
    )

    class Meta:
        verbose_name = "Produit"
        verbose_name_plural = "Produits"
        ordering = ['title']

    def __str__(self):
        return self.title
    
class News(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = "PUBLISHED", "Publié"
        ARCHIVED = "ARCHIVED", "Archivé"

    title = models.CharField(max_length=200)
    description = models.TextField()

    #image = models.ImageField(upload_to="news/", blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices, 
        default=Status.PUBLISHED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="news"
    )

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # if a user is deleted so are their favorites
        related_name="favorites"
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: # how the model behave
        unique_together = ['user', 'product'] # one user can add only once a product in favorite
        ordering = ['-created_at'] # favorites more recents first
        verbose_name = 'Favori' # names in django admin, in forms,..
        verbose_name_plural = 'Favoris'
    
    def __str__(self):
        return f"{self.user.first_name} - {self.product.title}"