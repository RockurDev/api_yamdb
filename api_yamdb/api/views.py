from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from users.permissions import (
    IsSuperuserOrAdmin,
    IsAdminOrReadOnly,
    IsOwner,
    IsOwnerOrReadOnly,
    IsModeratorOrReadOnly,
)
from reviews.models import Category, Genre, Title, Comment, Review
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class GenreViewSet(viewsets.ModelViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all().order_by('id')
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'delete']


class CategoryViewSet(viewsets.ModelViewSet):
    """Category viewset."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'patch', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset."""

    queryset = Title.objects.all().order_by('id')
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CommentSerializer
    search_fields = ('text',)

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review=review
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )
        return title.reviews.all()

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
