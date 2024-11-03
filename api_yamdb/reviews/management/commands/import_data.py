import os

from django.conf import settings
from django.core.management.base import BaseCommand

import pandas as pd

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


def get_data_frame(data_dir: str, filename: str) -> pd.DataFrame:
    file_path = os.path.join(data_dir, filename)
    return pd.read_csv(file_path)


class Command(BaseCommand):
    """Class implesments data parsing into a database."""

    def handle(self, *args, **kwargs) -> None:
        """Method for release imports."""

        data_dir = os.path.join(settings.BASE_DIR, 'static/data')

        self.import_categories(data_dir)
        self.import_genres(data_dir)
        self.import_titles(data_dir)
        self.import_genre_titles(data_dir)
        self.import_users(data_dir)
        self.import_reviews(data_dir)
        self.import_comments(data_dir)

    def import_categories(self, data_dir: str) -> None:
        """Import categories into database."""

        df = get_data_frame(data_dir, 'category.csv')
        for _, row in df.iterrows():
            Category.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )

    def import_genres(self, data_dir: str) -> None:
        """Import genres into database."""

        df = get_data_frame(data_dir, 'genre.csv')
        for _, row in df.iterrows():
            Genre.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )

    def import_titles(self, data_dir: str) -> None:
        """Import titles into database."""

        df = get_data_frame(data_dir, 'titles.csv')
        for _, row in df.iterrows():
            category = Category.objects.get(id=row['category'])
            Title.objects.get_or_create(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category=category,
            )

    def import_genre_titles(self, data_dir: str) -> None:
        """Import genre title into database."""

        df = get_data_frame(data_dir, 'genre_title.csv')
        for _, row in df.iterrows():
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)

    def import_users(self, data_dir: str) -> None:
        """Import users into database."""

        df = get_data_frame(data_dir, 'users.csv')
        for _, row in df.iterrows():
            User.objects.get_or_create(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                defaults={'is_staff': True, 'is_superuser': True},
            )

    def import_reviews(self, data_dir: str) -> None:
        """Import reviews into database."""

        df = get_data_frame(data_dir, 'review.csv')
        for _, row in df.iterrows():
            title = Title.objects.get(id=row['title_id'])
            author = User.objects.get(id=row['author'])
            Review.objects.get_or_create(
                id=row['id'],
                defaults={
                    'title': title,
                    'text': row['text'],
                    'author': author,
                    'score': row['score'],
                    'pub_date': row['pub_date'],
                },
            )

    def import_comments(self, data_dir: str) -> None:
        """Import comments into database."""

        df = get_data_frame(data_dir, 'comments.csv')
        for _, row in df.iterrows():
            review = Review.objects.get(id=row['review_id'])
            author = User.objects.get(id=row['author'])
            title = review.title
            Comment.objects.get_or_create(
                id=row['id'],
                review=review,
                defaults={
                    'title': title,
                    'text': row['text'],
                    'pub_date': row['pub_date'],
                    'author': author,
                },
            )
