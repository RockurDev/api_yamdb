from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import (
    Category,
    Genre,
    Title
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer
)


class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset for title, category, genre."""

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)

    def perform_create(self, serializer):
        category_slug = self.request.data.get('category')
        genre_slug = self.request.data.get('genre')
        category = get_object_or_404(
            Category, slug=category_slug
        )
        genre = get_object_or_404(
            Genre, slug=genre_slug
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        category_slug = self.request.data.get('category')
        genre_slug = self.request.data.get('genre')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            serializer.instance.category = category
        if genre_slug:
            genre = get_object_or_404(Genre, slug=genre_slug)
            serializer.instance.genre = genre
        serializer.save()


class GenreViewSet(BaseViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ('name',)


class CategoryViewSet(BaseViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ('name',)


class TitleViewSet(BaseViewSet):
    """Title viewset."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    search_fields = ('name', 'category__name', 'genre__name', 'year')
