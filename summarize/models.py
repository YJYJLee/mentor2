from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class post(models.Model):
    title = models.CharField(max_length=1024)
    body = models.TextField()
    author = models.ForeignKey(User)