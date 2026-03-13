from django.conf import settings
from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # if a user is deleted so are their favorites
        related_name="favorites",
    )
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="favorited_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:  # how the model behave
        unique_together = [
            "user",
            "product",
        ]  # one user can add only once a product in favorite
        ordering = ["-created_at"]  # favorites more recents first
        verbose_name = "Favori"  # names in django admin, in forms,..
        verbose_name_plural = "Favoris"

    def __str__(self):
        return f"{self.user.first_name} - {self.product.title}"
