from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class DesignRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('in_progress', 'Принято в работу'),
        ('done', 'Выполнено'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='requests/', help_text="jpg, jpeg, png, bmp")
    design_image = models.ImageField(upload_to='designs/', blank=True, null=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"


