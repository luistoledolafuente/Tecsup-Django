from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True)  # Puedes usar FontAwesome o similar

    def __str__(self):
        return self.name