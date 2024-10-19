from rest_framework import serializers

from .models import Category, Genre, Review, Title


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
    """Title Serializer."""

    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'category', 'genre')


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer."""

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)
