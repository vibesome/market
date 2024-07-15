from django.db import models
from django.contrib.auth.models import User

# Create your models here.







class Product(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    picture = models.ImageField(upload_to="product")
    created_at = models.DateTimeField(auto_now_add=True)
    ratings = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} by {self.owner.username}"
