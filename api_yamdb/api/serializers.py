from typing import OrderedDict
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Title, Review


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
        return average_rating if average_rating is not None else None

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

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField()
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                f'Отзыв на произведение {title.name} уже существует'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer."""

    class Meta:
        model = Comment
        fields = ('title_id', 'review_id', 'text')
