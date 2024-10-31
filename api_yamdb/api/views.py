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


class BaseViewSet(viewsets.ModelViewSet):
    """Read only for retrieve in genre and category."""

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']

    def retrieve(self, *args, **kwargs) -> Response:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(BaseViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer


class CategoryViewSet(BaseViewSet):
    """Category viewset."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset."""

    queryset = Title.objects.all().order_by('id')
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommentViewSet(viewsets.ModelViewSet):
    """ "Comment viewset."""

    queryset = Comment.objects.all().order_by('-pub_date')
    serializer_class = CommentSerializer
    permission_classes = [IsModeratorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    search_fields = ('text',)

    def perform_create(self, serializer: CommentSerializer) -> None:
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id)

        serializer.save(title=title, review=review, author=self.request.user)


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    queryset = Review.objects.all().order_by('-pub_date')
    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer: ReviewSerializer) -> None:
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
