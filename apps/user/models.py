from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserModel(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    creationDate = models.DateTimeField(auto_now_add=True)
    creator = models.OneToOneField(User, related_name='users', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name