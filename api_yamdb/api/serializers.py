import re
from typing import OrderedDict

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title

from users.models import CustomUser

User = get_user_model()

class GenreSerializer(serializers.ModelSerializer):
    """Genre Serializer."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    description = serializers.CharField(required=False)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def validate_genre(self, value: list) -> list:
        """Ensure that genre list is not empty."""
        if not value:
            raise serializers.ValidationError('This field must not be empty.')
        return value

    def get_rating(self, obj) -> float:
        average_rating = Review.objects.filter(title=obj).aggregate(
            Avg('score')
        )['score__avg']
        return average_rating if average_rating else None

    def to_representation(self, instance) -> OrderedDict:
        """Custom representation to intercept and modify output."""
        representation = super().to_representation(instance)

        representation['category'] = {
            'name': instance.category.name,
            'slug': instance.category.slug,
        }

        representation['genre'] = [
            {
                'name': genre.name,
                'slug': genre.slug,
            }
            for genre in instance.genre.all()
        ]

        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title')

    def validate(self, data) -> OrderedDict:
        """Check if the user already left a review about this title."""
        request = self.context.get('request')

        if request.method != 'POST':
            return data

        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(
            title__id=title_id, author=request.user
        ).exists():
            raise serializers.ValidationError(
                'You have already left a review about this work.'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('pub_date',)


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
                        'This email is already registered '
                        'with a different username.'
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
