from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import (
    Category,
    Genre,
    Title,
    Comment,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
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


class CommentViewSet(BaseViewSet):
    """ "Comment viewset."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    search_fields = ('text',)
    # permission_classes = []

    def perform_create(self, serializer) -> None:
        serializer.save(
            title_id=self.request.data.get('title_id'),
            review_id=self.request.data.get('review_id'),
        )
