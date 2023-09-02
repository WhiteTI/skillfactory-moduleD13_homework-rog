from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    confirmation_code = models.CharField(max_length=20)


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ad(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', default='images/default.jpg')

    def preview(self):
        return self.text[0:120] + '...'


class Review(models.Model):
    text = models.TextField()
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
