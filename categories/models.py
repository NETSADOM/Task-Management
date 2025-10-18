from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default="#007bff")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ['name', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.user.username}"