from rest_framework import serializers

from .models import Genre


class GenreSerializer(serializers.ModelSerializer):
    """Сериалайзер жанра."""
    class Meta:
        model = Genre
