from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .filters import TitleFilter
from .mixins import GenreCategoryBaseViewSet
from .permissions import IsSuperuserOrAdmin
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    UserSignUpSerializer,
)
from api.permissions import IsAdminOrReadOnly, IsModeratorOrReadOnly
from api.serializers import UserAccessTokenSerializer, UserSerializer
from reviews.models import Category, Genre, Review, Title

User = get_user_model()


@api_view(['POST'])
def signup(request: Request) -> Response:
    serializer = UserSignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
def get_jwt_token(request: Request) -> Response:
    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)

    token = AccessToken.for_user(user)

    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuserOrAdmin]
    http_method_names = ('get', 'post', 'patch', 'delete')
    lookup_field = 'username'
    search_fields = ('role', 'username')

    @action(
        detail=False,
        url_path='me',
        methods=['GET', 'PATCH'],
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: Request) -> Response:
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
        else:
            serializer = UserSerializer(
                self.request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)

        return Response(serializer.data, status=status.HTTP_200_OK)


class GenreViewSet(GenreCategoryBaseViewSet):
    """Genre viewset."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(GenreCategoryBaseViewSet):
    """Category viewset."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Title viewset."""

    queryset = (
        Title.objects.all()
        .order_by('name')
        .annotate(rating=Avg('reviews__score'))
    )
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = TitleFilter
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    http_method_names = ('get', 'post', 'patch', 'delete')


class CommentViewSet(viewsets.ModelViewSet):
    """Comment viewset."""

    serializer_class = CommentSerializer
    permission_classes = [IsModeratorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')
    search_fields = ('text',)

    def get_queryset(self):
        return self.get_review().comments.order_by('-pub_date')

    def get_review(self) -> Review:
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )

    def perform_create(self, serializer: CommentSerializer) -> None:
        review = self.get_review()
        serializer.save(
            title=review.title, review=review, author=self.request.user
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Review viewset."""

    serializer_class = ReviewSerializer
    permission_classes = [IsModeratorOrReadOnly, IsAuthenticatedOrReadOnly]
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_title(self) -> Title:
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer: ReviewSerializer) -> None:
        serializer.save(author=self.request.user, title=self.get_title())
