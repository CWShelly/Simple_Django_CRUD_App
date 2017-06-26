from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200, default='Default Value')

    def __str__(self):
        return self.title 
