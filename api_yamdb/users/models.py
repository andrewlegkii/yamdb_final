from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICES = (
    (ADMIN, 'Администратор'),
    (MODERATOR, 'Модератор'),
    (USER, 'Пользователь')
)


class User(AbstractUser):
    bio = models.TextField(
        blank=True,
        default='',
        verbose_name='Биография'
    )
    email = models.EmailField(
        max_length=settings.LIMIT_EMAIL,
        unique=True,
        verbose_name='Электронная почта'
    )
    role = models.CharField(
        choices=ROLE_CHOICES,
        default=USER,
        max_length=settings.LIMIT_USER_CHAT,
        verbose_name='Статус прав'
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
