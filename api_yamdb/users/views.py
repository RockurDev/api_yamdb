from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny

from users.permissions import (
    IsAdminOrReadOnly,
    IsModeratorOrReadOnly,
    IsOwnerOrReadOnly,
    IsSuperuserOrAdmin
)
from .models import CustomUser
from .serializers import (
    UserAccessTokenSerializer,
    UserCreationSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsSuperuserOrAdmin]

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
    user = get_object_or_404(CustomUser, username=username)

    token = AccessToken.for_user(user)

    return Response({'token': str(token)}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request: Request) -> Response:
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()

    confirmation_code = default_token_generator.make_token(user)

    send_mail(
        'Confirmation code',
        f'Your confirmation code is {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

    return Response(
        {'username': user.username, 'email': user.email},
        status=status.HTTP_200_OK,
    )
