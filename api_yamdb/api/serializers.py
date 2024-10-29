from typing import OrderedDict
from django.db.models import Avg
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

    author = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'title')


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer."""

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date')
        read_only_fields = ('title_id', 'review_id', 'author', 'pub_date')
