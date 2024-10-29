from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework import viewsets

from .filters import TitleFilter
from users.permissions import (
    IsOwner,
    IsSuperuserOrAdmin,
    IsAdminOrReadOnly,
    IsOwnerOrReadOnly,
    IsModeratorOrReadOnly,
)

from reviews.models import Category, Genre, Title, Review, Comment

from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    """Read only for retrieve in genre and category."""

    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']

    def retrieve(self, request, *args, **kwargs):
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
    search_fields = (
        'name',
        'category__name',
        'genre__name',
        'genre__slug',
        'year',
    )
    filterset_fields = [
        'name',
        'year',
        'category__name',
        'genre__name',
        'genre__slug',
    ]
    http_method_names = ['get', 'post', 'patch', 'delete']


class CommentViewSet(viewsets.ModelViewSet):
    """ "Comment viewset."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsSuperuserOrAdmin | IsOwner]
    http_method_names = ['get', 'post', 'patch', 'delete']

    search_fields = ('text',)

    def perform_create(self, serializer) -> None:
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')

        title = get_object_or_404(Title, id=title_id)
        review = get_object_or_404(Review, id=review_id)

        serializer.save(title=title, review=review, author=self.request.user)
    


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsSuperuserOrAdmin | IsOwner]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        serializer.save(
            author=self.request.user,
            title=title
        )

    class Meta:
        read_only_fields = ('author',)
