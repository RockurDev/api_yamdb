from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdminOrReadOnly, IsModeratorOrReadOnly

from .filters import TitleFilter
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
)
from reviews.models import Category, Comment, Genre, Review, Title
from .mixins import GenreCategoryBaseViewSet


class GenreViewSet(GenreCategoryBaseViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryViewSet(GenreCategoryBaseViewSet):
    """Category viewset."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset."""

    queryset = Title.objects.all().order_by('name')
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    http_method_names = ('get', 'post', 'patch', 'delete')


class CommentViewSet(viewsets.ModelViewSet):
    """ "Comment viewset."""

    serializer_class = CommentSerializer
    permission_classes = [IsModeratorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')

    search_fields = ('text',)

    def get_queryset(self):
        return Comment.objects.all().order_by('-pub_date')

    def perform_create(self, serializer: CommentSerializer) -> None:
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        review = get_object_or_404(Review, id=review_id, title_id=title_id)

        serializer.save(
            title=review.title, review=review, author=self.request.user
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return Review.objects.all().order_by('-pub_date')

    def perform_create(self, serializer: ReviewSerializer) -> None:
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
