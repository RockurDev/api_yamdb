from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models

ANONYM = 'anonym'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = [
    (ANONYM, 'Anonymous'),
    (USER, 'User'),
    (MODERATOR, 'Moderator'),
    (ADMIN, 'Admin'),
]


class BaseUser:
    """
    A base class for user properties and methods.
    This class does not inherit from models.Model, so no extra table is created.
    """

    @property
    def is_admin(self) -> bool:
        return any([self.role == ADMIN, self.is_superuser, self.is_staff])

    @property
    def is_moderator(self) -> bool:
        return self.role == MODERATOR

    @property
    def is_user(self) -> bool:
        return self.role == USER

    def __str__(self) -> str:
        return self.username


class CustomUser(AbstractBaseUser, BaseUser):
    """
    Custom user model inheriting from AbstractBaseUser and BaseUser.
    This model is the one that will create a table in the database.
    """

    objects = UserManager()

    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)
    is_superuser = models.BooleanField(
        verbose_name='Is Superuser', default=False
    )

    username = models.SlugField(
        max_length=150, unique=True, verbose_name='Слаг'
    )
    first_name = models.CharField(
        max_length=150, blank=True, verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150, blank=True, verbose_name='Фамилия'
    )
    email = models.EmailField(
        max_length=254, unique=True, verbose_name='Электронная почта'
    )
    bio = models.TextField(blank=True, verbose_name='Биография')
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=USER, verbose_name='Роль'
    )
    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=200,
        editable=False,
        null=True,
        blank=True,
        unique=True,
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta(AbstractBaseUser.Meta):
        app_label = 'users'
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_username_email'
            )
        ]
