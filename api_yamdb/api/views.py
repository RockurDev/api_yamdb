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

    serializer_class = TitleSerializer
    search_fields = ('name', 'category__name', 'genre__name', 'year')

    def get_queryset(self):
        return Title.objects.select_related('category', 'genre')
