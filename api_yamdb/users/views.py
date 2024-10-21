from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny

from api.permissions import IsAdmin
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
    permission_classes = [IsAdmin]
    lookup_field = 'username'

    @action(methods=['patch', 'get'], detail=False, url_path='me',
            permission_classes=[permissions.IsAuthenticated])
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
def signup(request):
    serializer = UserCreationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    if (
        CustomUser.objects.filter(email=email).exists()
        or CustomUser.objects.filter(username=username).exists()
    ):
        return Response(status=status.HTTP_400_BAD_REQUEST)
    user, code_created = CustomUser.objects.get_or_create(
        email=email, username=username)
    confirmation_code = default_token_generator.make_token(user)
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        'Confirmation code',
        f'Your code {confirmation_code}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False
    )
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = UserAccessTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(user, username=username)
    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
