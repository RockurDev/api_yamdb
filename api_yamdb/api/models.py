from django.db import models


class BaseModel(models.Model):
    """Basemodel for genre, category."""

    name = models.CharField(
        max_length=256,
        blank=False,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
        verbose_name='Слаг'
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
        verbose_name='Название'
    )
    description = models.TextField(
        max_length=256,
        verbose_name='Описание'
    )
    year = models.IntegerField(
        verbose_name='Год'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
