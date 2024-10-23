from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets

from api_yamdb.users.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from reviews.models import Category, Genre, Title, Comment
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset for title, category, genre."""

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)


class GenreViewSet(BaseViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    search_fields = ('name',)


class CategoryViewSet(BaseViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    search_fields = ('name',)


class TitleViewSet(BaseViewSet):
    """Title viewset."""

    queryset = Title.objects.select_related('category', 'genre')
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TitleSerializer
    search_fields = ('name', 'category__name', 'genre__name', 'year')


class CommentViewSet(BaseViewSet):
    """ "Comment viewset."""

    queryset = Comment.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    search_fields = ('text',)
    # permission_classes = []

    def perform_create(self, serializer) -> None:
        serializer.save(
            title_id=self.request.data.get('title_id'),
            review_id=self.request.data.get('review_id'),
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_title(self) -> Title:
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews

    def perform_create(self, serializer) -> None:
        # TODO: connect with custom user
        # serializer.save(
        #     title_id=self.kwargs.get('title_id'),
        #     author=get_user_model().objects.get(pk=1),
        # )
        serializer.save(
            title_id=self.kwargs.get('title_id'), author=self.request.user
        )

    class Meta:
        read_only_fields = ('author',)
