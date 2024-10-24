import re

from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to transform User instances
    to and from JSON. This covers fields like first name, last name,
    username, bio, email, and role.
    """

    class Meta:
        model = CustomUser
        exclude = ('confirmation_code',)


class UserCreationSerializer(serializers.ModelSerializer):
    """
    Serializer to handle user creation. Expects an email and username as input.
    """

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    def validate_username(self, value) -> str:
        if len(value) > 150 or value == 'me':
            raise serializers.ValidationError(
                {'email': 'Choose another username'}
            )

        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                {'username': 'Username contains not allowed symbols.'}
            )

        return value

    def validate(self, data):
        username = data['username']
        email = data['email']

        if CustomUser.objects.filter(username=username).exists():
            user = CustomUser.objects.get(username=username)

            if user.email == email:
                if not CustomUser.objects.filter(email=email).exists():
                    raise serializers.ValidationError(
                        {'username': 'Choose another username.'}
                    )
                else:
                    raise serializers.ValidationError(
                        {
                            'username': 'Choose another username.',
                            'email': email,
                        }
                    )

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            if user.username != username:
                raise serializers.ValidationError(
                    {
                        'email': 'This email is already registered with a different username.'
                    }
                )

        return data

    def validate_email(self, value):
        if len(value) > 254:
            raise serializers.ValidationError(
                'Содержимое "email" не должно превышать 254 символа'
            )
        return value

    class Meta:
        model = CustomUser
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

    def validate(self, data):
        user = get_object_or_404(CustomUser, username=data['username'])

        if not default_token_generator.check_token(
            user, data['confirmation_code']
        ):
            raise serializers.ValidationError(
                {'confirmation_code': 'Invalid verification code'}
            )

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
