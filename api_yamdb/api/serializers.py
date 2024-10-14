from rest_framework import serializers

from .models import Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанра."""
    class Meta:
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер категории."""
    class Meta:
        model = Category
