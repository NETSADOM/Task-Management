from django.db import models
from django.contrib.auth.models import User
from categories.models import Category
from django.utils import timezone

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    due_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tasks'
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['due_date']),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    def mark_complete(self):
        self.status = 'completed'
        self.completed_at = timezone.now()
        self.save()
    
    def mark_incomplete(self):
        self.status = 'pending'
        self.completed_at = None
        self.save()