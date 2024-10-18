from django.contrib import admin

from .models import Category, Genre, Title


class BaseAdmin(admin.ModelAdmin):
    """Base admin model for genre and category."""

    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_editable = ('slug',)


@admin.register(Genre)
class GenreAdmin(BaseAdmin):
    """Admin model genre."""

    pass


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    """Admin model category."""

    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Admin model title."""

    list_display = ('name', 'description', 'category', 'year')
    search_fields = ('name', 'category', 'genre', 'year')
    list_editable = ('description', 'category', 'year')
