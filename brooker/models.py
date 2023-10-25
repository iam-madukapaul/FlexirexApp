from django.db import models
from profiles.models import UserProfile

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='img')
    body = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title
    

class Home(models.Model):
    total_rewards = models.CharField(max_length=9)
    total_investor = models.CharField(max_length=9)
    total_withdraw = models.CharField(max_length=9)
    total_transaction = models.CharField(max_length=9)

    def __str__(self):
        return f"Home - {self.total_rewards}"

