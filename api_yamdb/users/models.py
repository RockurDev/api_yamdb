import re
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models


# ANONIM = 'anonim'
ANONIM = 'anonym'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


# CHOICES = [
#     ('anon', ANONIM),
#     ('admin', ADMIN),
#     ('moderator', MODERATOR),
#     ('user', USER),
# ]


CHOICES = [
    (ANONIM, 'Anonymous'),
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin'),
]


class CustomUser(AbstractBaseUser):
    objects = UserManager()

    is_staff = models.BooleanField(verbose_name='Is Staff')
    is_superuser = models.BooleanField(verbose_name='Is Superuser')

    username = models.SlugField(max_length=150, verbose_name='Слаг')
    first_name = models.CharField(
        verbose_name='Введите имя', max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True, null=True
    )
    email = models.EmailField(max_length=254, verbose_name='Электронная почта')
    bio = models.TextField(verbose_name='Биография', blank=True, null=True)
    role = models.CharField(
        verbose_name='Роль', choices=CHOICES, default=USER, max_length=10
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True,
    )

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self) -> bool:
        return any([self.role == ADMIN, self.is_superuser, self.is_staff])

    @property
    def is_moderator(self) -> bool:
        return self.role == MODERATOR

    class Meta(AbstractBaseUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]

    def __str__(self) -> str:
        return self.username
