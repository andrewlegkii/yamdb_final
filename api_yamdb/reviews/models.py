from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title
from users.models import User


class Review(models.Model):
    text = models.CharField(
        max_length=256,
        verbose_name='Текст',
        help_text='Тест отзыва',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='review',
        null=True,
        verbose_name='Автор',
        help_text='Автор отзыва',
    )
    score = models.PositiveSmallIntegerField(
        default=None,
        validators=(MinValueValidator(1), MaxValueValidator(10)),
        verbose_name='Оценка',
        help_text='Оставьте оценку'
    )
    pub_date = models.DateTimeField(
        'Дата',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        verbose_name='Произведение',
        help_text='Название произведения',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_review_author'
            ),
        )
        ordering = ('id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    text = models.CharField(
        max_length=256,
        verbose_name='Комментарий',
        help_text='Напишите ваш комментарий'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comment',
        null=True,
        verbose_name='Автор',
        help_text='Автор комментария',
    )
    pub_date = models.DateTimeField(
        'Дата',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comment',
        null=True,
        verbose_name='Отзыв',
        help_text='Отзыв о произведении'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:20]
