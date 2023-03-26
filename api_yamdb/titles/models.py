from datetime import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории',
        help_text='Название категории',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug для категории',
        help_text='Slug для категории',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:20]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра',
        help_text='Название жанра',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug для жанра',
        help_text='Slug для жанра',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:20]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Название произведения',
    )
    year = models.PositiveSmallIntegerField(
        validators=(MaxValueValidator(dt.now().year),),
        verbose_name='Год',
        help_text='Год издания',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Описание',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория',
        help_text='Название Категории',
    )
    rating = models.PositiveSmallIntegerField(
        default=None,
        blank=True,
        null=True,
        verbose_name='Оценка',
        help_text='Рейтинг произведения',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:20]
