from django.conf import settings
from django.db import models


class News(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "PUBLISHED", "Publié"
        ARCHIVED = "ARCHIVED", "Archivé"

    title = models.CharField(max_length=200)
    description = models.TextField()

    # image = models.ImageField(upload_to="news/", blank=True, null=True)

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PUBLISHED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="news",
    )

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
