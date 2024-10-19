from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from django.contrib.auth import get_user_model
from .models import Category, Genre, Title
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
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

    queryset = Title.objects.select_related('category', 'genre')
    serializer_class = TitleSerializer
    search_fields = ('name', 'category__name', 'genre__name', 'year')


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    # TODO
    # permission_classes = []

    def get_title(self) -> Title:
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews
˝˝
    def perform_create(self, serializer) -> None:
        # TODO: connect with custom user
        serializer.save(
            title_id=self.kwargs.get('title_id'),
            author=get_user_model().objects.get(pk=1),
        )
        # serializer.save(title_id = self.kwargs.get('title_id'),author=self.request.user)

    class Meta:
        read_only_fields = ('author',)
