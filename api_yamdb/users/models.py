from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


ANONIM = 'anonim'
USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'


CHOICES = [
    ('anon', ANONIM),
    ('admin', ADMIN),
    ('moderator', MODERATOR),
    ('user', USER),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    username = models.SlugField(max_length=150, unique=True, verbose_name='Слаг')
    first_name = models.CharField(
        verbose_name='Введите имя', max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        verbose_name='Фамилия', max_length=150, blank=True, null=True
    )
    email = models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')
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

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
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
