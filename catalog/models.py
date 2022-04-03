from django.db import models
from django.urls import reverse
from django.conf.global_settings import LANGUAGES
from django.utils.text import slugify


class Author(models.Model):
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField(null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        return reverse('author-detail', args=self.slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.last_name + ' ' + self.first_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.ManyToManyField(Author)
    publication_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, help_text='13 Character ISBN number', null=True, blank=True)
    number_of_pages = models.IntegerField(null=True, blank=True)
    cover = models.URLField(null=True, blank=True)
    language = models.CharField(max_length=7, choices=LANGUAGES, null=True, blank=True)

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('book-detail', args=self.isbn)

    def __str__(self):
        return f'{self.title} - {self.author}'
