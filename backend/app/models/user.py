from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # In abstractUser there are already all user infos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username