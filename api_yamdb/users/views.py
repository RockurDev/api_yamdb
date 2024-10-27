from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated

from .permissions import IsSuperuserOrAdmin

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
    http_method_names = ['get', 'post', 'patch', 'delete']
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
            data = request.data.copy()

            # Prevent role from being changed
            if 'role' in data and request.user.role != data['role']:
                data.pop('role')

            serializer = UserSerializer(
                self.request.user, data=data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request: Request) -> Response:
    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)

    token = AccessToken.for_user(user)

    return Response({'token': str(token)}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request: Request) -> Response:
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # If the user does not exists and requests confirmation code
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
