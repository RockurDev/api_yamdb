from rest_framework import serializers

from .models import Category, Genre, Title


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
