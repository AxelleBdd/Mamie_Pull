from django.db import models
from django.conf import settings

class News(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = "PUBLISHED"
        ARCHIVED = "ARCHIVED"

    title = models.CharField(max_length=200)
    description = models.TextField()

    status = models.CharField(
        choices=Status.choices, 
        default=Status.PUBLISHED
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #image = models.ImageField(upload_to="news/")

    created_by = models.ForeignKey(
        #settings.AUTH_USER_MODEL, #authenticate admin user
        on_delete=models.SET_NULL,
        null=True,
        blnk=True,
        related_name="news"
    )

    def __str__(self):
        return self.title