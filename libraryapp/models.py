from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime
from django.utils import timezone


class User(AbstractUser):
    pass


class Key(models.Model):
    key = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.key}"


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name}"


class Subcategory(models.Model):
    name = models.CharField(max_length=30)
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.name}"


class Post(models.Model):
    subcategory = models.ForeignKey(
        'Subcategory', on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='author_post')
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(
        upload_to='', null=True, blank=True)

    def __str__(self):
        return f"In {self.subcategory} - by {self.user}: {self.content}"


class Reading(models.Model):
    subcategory = models.ForeignKey(
        'Subcategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    author = models.CharField(max_length=80)
    year = models.CharField(max_length=80)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='author_reading')
    date = models.DateTimeField(default=timezone.now)
    pdf = models.FileField(upload_to='readings/pdfs/')
    cover = models.ImageField(
        upload_to='', null=True, blank=True)
    liked_readings = models.ManyToManyField(
        'User', default=None, blank=True, related_name='reading_liked')

    def __str__(self):
        return f" {self.subcategory} - '{self.title}', by {self.author}"


class Review(models.Model):
    reading = models.ForeignKey(
        'Reading', on_delete=models.CASCADE)
    content = models.CharField(max_length=400)
    image = models.ImageField(
        upload_to='', null=True, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='author_review')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.reading} - '{self.content}', by {self.user}"


class Image(models.Model):
    subcategory = models.ForeignKey(
        'Subcategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    image = models.ImageField(
        upload_to='', null=True, blank=True)
    description = models.CharField(max_length=400, null=True, blank=True)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='author_image')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.subcategory} - '{self.title}', by {self.user}"


class Film(models.Model):
    subcategory = models.ForeignKey(
        'Subcategory', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    link = models.CharField(max_length=400)
    description = models.CharField(max_length=400)
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='author_film')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.subcategory} - '{self.title}', by {self.user}"
