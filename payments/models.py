from django.db import models

# Create your models here.

class paymentRequests(models.Model):
    owner = models.ForeignKey('home.CustomUser', on_delete=models.CASCADE)
    amount = models.FloatField()
    phone = models.CharField(max_length=255)
    narrative = models.TextField()
    status = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    