from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contacts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

class Messages(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()

class Blogs(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='pics')
    main_para = models.TextField()
    heading1 = models.CharField(max_length=100, blank=True, null=True)
    para1 = models.TextField(blank=True, null=True)
    heading2 = models.CharField(max_length=100, blank=True, null=True)
    para2 = models.TextField(blank=True, null=True)
    isApproved = models.BooleanField(default=False)

class Campaign(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()

class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'campaign')