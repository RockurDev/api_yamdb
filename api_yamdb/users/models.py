from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from users.validators import validate_username


class User(AbstractUser):
    """This model creates a user table in the database."""

    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    is_staff = models.BooleanField(verbose_name='Is Staff', default=False)

    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        verbose_name='Username',
        validators=[validate_username],
    )
    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH, unique=True, verbose_name='Email'
    )
    bio = models.TextField(blank=True, verbose_name='Bio')
    role = models.CharField(
        max_length=max(map(len, Role.values)),
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Role',
    )

    class Meta(AbstractUser.Meta):
        app_label = 'users'
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_admin(self) -> bool:
        return any(
            [self.role == self.Role.ADMIN, self.is_superuser, self.is_staff]
        )

    @property
    def is_moderator(self) -> bool:
        return self.role == self.Role.MODERATOR

    def __str__(self) -> str:
        return self.username
