from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # In abstractUser there are already all user infos (username, first_name, last_name, password, is_staff, created_at = date_joined)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username