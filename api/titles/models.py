from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Titles(models.Model):
    name = models.CharField(max_length=30, unique=False)
    year = models.PositiveSmallIntegerField(null=True)
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True, max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="categories", null=True)
    genre = models.ManyToManyField(Genre, related_name="genres", blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='reviews')
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(verbose_name='Введите оценку от 1 до 10',
                                validators=[MinValueValidator(1), MaxValueValidator(10)])
    pub_date = models.DateTimeField('review date', auto_now_add=True)

    class Meta:
        # constraints = [models.UniqueConstraint(fields=['title', 'author'], name='unique_review')]
        ordering = ['pub_date']

    def __str__(self):
        return self.text


class Comment(models.Model):
    # title = models.ForeignKey(Titles, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('comment date', auto_now_add=True)

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
