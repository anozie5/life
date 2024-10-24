from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# user model
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    age = models.IntegerField(null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    


# token record
class Token(models.Model):
    users = models.OneToOneField(User, on_delete=models.CASCADE)
    tokens = models.IntegerField()

    def __str__(self):
        return self.tokens