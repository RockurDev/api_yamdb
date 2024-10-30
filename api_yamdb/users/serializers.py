import re
from typing import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import CustomUser

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """
    A base class for user properties and methods.
    This class does not inherit from models.Model,
    so no extra table is created.
    """

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_email(self, value: str) -> str:
        if len(value) > 254:
            raise serializers.ValidationError(
                {'email': 'Choose another email'}
            )
        return value

    def validate_username(self, value: str) -> str:
        if len(value) > 150 or value == 'me':
            raise serializers.ValidationError(
                {'username': 'Choose another username'}
            )

        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                'Username contains not allowed symbols'
            )

        return value

    def validate(self, data: OrderedDict) -> OrderedDict:
        username = data.get('username')
        email = data.get('email')

        # Check if a user exists with the same username
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            # If the email is not registred
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {'username': 'Choose another username'}
                )

            # If the email does not match the registered user's email
            if email != user.email:
                raise serializers.ValidationError(
                    {'username': 'Choose another username.', 'email': email}
                )

        # Check if any user exists with the same email but different username
        if (
            User.objects.filter(email=email)
            .exclude(username=username)
            .exists()
        ):
            raise serializers.ValidationError(
                {
                    'email': (
                        'This email is already registered with a different username.'
                    )
                }
            )

        return data


class UserSerializer(BaseUserSerializer):
    """
    Serializer for the User model to transform User instances
    to and from JSON. This covers fields like first name, last name,
    username, bio, email, and role.
    """

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'role',
            'first_name',
            'last_name',
            'bio',
        )


class UserCreationSerializer(BaseUserSerializer):
    """
    Serializer to handle user creation. Expects an email and username as input.
    """

    def get_or_create(self) -> CustomUser:
        instance, _ = User.objects.get_or_create(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        return instance

    class Meta:
        model = User
        fields = ['email', 'username']
        extra_kwargs = {'password': {'write_only': True}}


class UserAccessTokenSerializer(serializers.ModelSerializer):
    """
    Serializer for handling user access token validation.
    Expects a username and a confirmation code as input.

    Validates the confirmation code against the stored token for the user.
    """

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, data: OrderedDict) -> OrderedDict:
        user = get_object_or_404(User, username=data['username'])

        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Invalid verification code'}
            )

        return data

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
