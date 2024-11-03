from typing import OrderedDict

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.constants import MAX_EMAIL_LENGTH, MAX_USERNAME_LENGTH
from users.validators import validate_username


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


class TitleReadSerializer(serializers.ModelSerializer):
    """Serializer for reading Title."""

    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""

    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
        allow_null=False,
        allow_empty=False
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
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

    def get_rating(self, obj) -> float:
        average_rating = Review.objects.filter(title=obj).aggregate(
            Avg('score')
        )['score__avg']
        return average_rating if average_rating else None

    def to_representation(self, instance) -> OrderedDict:
        """Custom representation to intercept and modify output."""
        representation = super().to_representation(instance)

        read_serializer = TitleReadSerializer(instance)
        representation = read_serializer.data

        return representation


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer."""

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)

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

    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSignUpSerializer(serializers.Serializer):
    """A base class for user properties and methods."""

    email = serializers.EmailField(required=True, max_length=MAX_EMAIL_LENGTH)
    username = serializers.CharField(
        required=True,
        validators=[validate_username],
        max_length=MAX_USERNAME_LENGTH,
    )

    def validate(self, data: OrderedDict) -> OrderedDict:
        username = data.get('username')
        email = data.get('email')

        user_by_username = User.objects.filter(username=username).first()
        user_by_email = User.objects.filter(email=email).first()

        if user_by_username != user_by_email:
            if user_by_username:
                raise serializers.ValidationError(
                    {'username': 'Choose another username.'}
                )
            if user_by_email:
                raise serializers.ValidationError(
                    {
                        'email': (
                            'This email is already registered '
                            'with a different username.'
                        )
                    }
                )

        return data

    def create(self, validated_data):
        user, _ = User.objects.get_or_create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'API_YAMDB. Confirmation code',
            f'Your confirmation code: {confirmation_code}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return user


class UserSerializer(serializers.ModelSerializer):
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


class UserAccessTokenSerializer(serializers.Serializer):
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
