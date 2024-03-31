import uuid

from django.conf.global_settings import AUTH_USER_MODEL
from django.db import models


# Create your models here.
class Movie(models.Model):
    GENRE_CHOICES = (
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('science-fiction', 'Science Fiction'),
        ('fantasy', 'Fantasy'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    length = models.PositiveIntegerField()
    image_card = models.ImageField(upload_to='movie_images')
    image_cover = models.ImageField(upload_to='movie_images')
    video = models.FileField(upload_to="movie_videos")
    movie_views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class MovieList(models.Model):
    owner = models.ForeignKey(to=AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Movie Lists'

    def __str__(self):
        return f'Movie: {self.movie.primary_key:>3} | Owner: {self.owner.primary_key:>3}'
