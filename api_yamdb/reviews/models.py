from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    MAX_NAME_LENGTH,
    MAX_TEXT_LENGTH,
    MAX_NUMB,
    MIN_NUMB,
)
from reviews.validators import validate_past_year

User = get_user_model()


class BaseModel(models.Model):
    """Basemodel for genre, category."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Название',
    )
    slug = models.SlugField(
        max_length=MAX_TEXT_LENGTH,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        ordering = ('name',)
        abstract = True

    def __str__(self) -> str:
        return self.name[:MAX_NAME_LENGTH]


class Genre(BaseModel):
    """Model Genre."""

    class Meta(BaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(BaseModel):
    """Model Category."""

    class Meta(BaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    """Model Title."""

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        verbose_name='Название',
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание',
    )
    year = models.SmallIntegerField(
        validators=[validate_past_year],
        verbose_name='Год',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['name']

    def __str__(self) -> str:
        return self.name[:MAX_NAME_LENGTH]


class Review(models.Model):
    """Review model."""

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
    score = models.IntegerField(
        null=True,
        validators=[
            MaxValueValidator(
                MAX_NUMB, message='The rating should not be higher than 10'
            ),
            MinValueValidator(
                MIN_NUMB, message='The rating must be at least 1'
            ),
        ],
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
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], name='unique_review'
            )
        ]
        ordering = ['-pub_date']


class Comment(models.Model):
    """Comment model."""

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Произведение'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments', verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self) -> str:
        return self.text[MAX_TEXT_LENGTH]
