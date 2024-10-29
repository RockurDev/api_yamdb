from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from .filters import TitleFilter
from users.permissions import (
    IsSuperuserOrAdmin,
    IsAdminOrReadOnly,
    IsOwner,
    IsOwnerOrReadOnly,
)
from reviews.models import Category, Genre, Title, Comment
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
    permission_classes = [IsAdminOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    search_fields = ('text',)

    def perform_create(self, serializer) -> None:
        serializer.save(
            title_id=self.request.data.get('title_id'),
            review_id=self.request.data.get('review_id'),
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    permission_classes = [IsSuperuserOrAdmin | IsOwner]
    # lookup_field = 'title_id'

    # def get_title(self) -> Title:
    #     return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    # def get_queryset(self):
    #     return self.get_title().reviews

    def perform_create(self, serializer) -> None:
        serializer.save(
            title_id=self.kwargs.get('title_id'),
            author=self.request.user,
        )

    class Meta:
        read_only_fields = ('author',)
