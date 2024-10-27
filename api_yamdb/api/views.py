from django_filters.rest_framework import CharFilter, DjangoFilterBackend, FilterSet
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from users.permissions import (
    IsSuperuserOrAdmin,
    IsOwnerOrReadOnly,
    IsAdminOrReadOnly,
    IsModeratorOrReadOnly
)
from reviews.models import Category, Genre, Title, Comment
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleCreateSerializer,
    CommentSerializer,
    ReviewSerializer,
)


class BaseViewSet(viewsets.ModelViewSet):
    """Base viewset for title, category, genre."""

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)


class GenreViewSet(BaseViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all().order_by('id')
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    serializer_class = GenreSerializer
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if not Genre.objects.filter(slug=slug).exists():
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().retrieve(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        if not Genre.objects.filter(slug=slug).exists():
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().partial_update(request, *args, **kwargs)


class CategoryViewSet(BaseViewSet):
    """Category viewset."""

    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method Not Allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {'detail': 'Method Not Allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(BaseViewSet):
    """Title viewset."""

    queryset = Title.objects.select_related('category', 'genre')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    serializer_class = TitleSerializer
    search_fields = ('name', 'category__name', 'genre__name', 'year')

    def get_queryset(self):
        return Title.objects.all()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_admin:
            return super().partial_update(request, *args, **kwargs)
        return Response(
            {'detail': 'Method Not Allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return TitleCreateSerializer
        return TitleSerializer


class CommentViewSet(BaseViewSet):
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
    permission_classes = [IsAdminOrReadOnly, IsOwnerOrReadOnly]

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
