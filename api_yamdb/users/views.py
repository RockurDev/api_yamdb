from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import (
    IsSuperuserOrAdmin,
    IsOwnerOrReadOnly
)

from .serializers import (
    UserAccessTokenSerializer,
    UserCreationSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperuserOrAdmin]
    lookup_field = 'username'
    search_fields = ('role',)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_param = self.request.query_params.get('search', None)
        if search_param:
            queryset = queryset.filter(username__icontains=search_param)
        return queryset

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(
                {'detail': 'Method Not Allowed'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        return super().update(request, *args, **kwargs)

    @action(methods=['patch', 'get'], detail=False, url_path='me')
    def me(self, request: Request) -> Response:
        if request.method == 'GET':
            serializer = UserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = UserSerializer(self.request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(partial=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request: Request) -> Response:
    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)

    token = AccessToken.for_user(user)

    return Response({'token': str(token)}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request: Request) -> Response:
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # If the user not exists and requests confirmation code
    user = serializer.get_or_create()

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'API_YAMDB. Confirmation code',
        f'Your confirmation code: {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return Response(
        {'username': user.username, 'email': user.email},
        status=status.HTTP_200_OK,
    )
