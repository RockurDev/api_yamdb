from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Title, Review


class GenreSerializer(serializers.ModelSerializer):
    """Genre Serializer."""

    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Category Serializer."""

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """Title Serializer."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
        model = Title
        fields = ('name', 'description', 'year', 'category', 'genre', 'id')


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True
    )

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'category', 'genre', 'id')


class ReviewSerializer(serializers.ModelSerializer):
    """Review Serializer."""

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author',)


class CommentSerializer(serializers.ModelSerializer):
    """Comment Serializer."""

    class Meta:
        model = Comment
        fields = ('title_id', 'review_id', 'text')
