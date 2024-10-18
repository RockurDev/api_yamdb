from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()

MAX_TEXT_LENGTH = 40


class BaseModel(models.Model):
    """Basemodel for genre, category."""

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModel):
    """Model Genre."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseModel):
    """Model Category."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Model Title."""

    name = models.CharField(
        max_length=100,
        verbose_name='Название',
    )
    description = models.TextField(
        max_length=256,
        verbose_name='Описание',
    )
    year = models.IntegerField(
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='reviews',
    )
    score = models.SmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    def __str__(self) -> str:
        return self.text[:MAX_TEXT_LENGTH]

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
