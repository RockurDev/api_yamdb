from django.contrib.auth.models import AbstractUser
from django.db import models


ANONIM = 'anonim'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


CHOICES = [
    ('anon', ANONIM),
    ('admin', ADMIN),
    ('moderator', MODERATOR),
    ('user', USER)
]


class User(AbstractUser):
    first_name = models.CharField(
        verbose_name='Введите имя',
        max_length=20,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        verbose_name='Введите фамилию'
        max_length=20,
        blank=True,
        null=True
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        unique=True
    )
    bio = models.CharField(
        verbose_name='Биография',
        max_length=100,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=CHOICES,
        default=USER,
        max_length=10
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True
    )

    @property
    def is_admin(self):
        return any(
            [self.role == ADMIN, self.is_superuser, self.is_staff]
        )

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
