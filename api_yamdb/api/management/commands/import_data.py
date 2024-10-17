import os

import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings

from api.models import Category, Genre, Title


class Command(BaseCommand):
    """Class implesments data parsing into a database."""

    def handle(self, *args, **kwargs):
        """Method for release imports."""
        data_dir = os.path.join(settings.BASE_DIR, 'static/data')
        self.import_categories(data_dir)
        self.import_genres(data_dir)
        self.import_titles(data_dir)
        self.import_genre_titles(data_dir)

    def import_categories(self, data_dir):
        """Import categories into database."""
        file_path = os.path.join(data_dir, 'category.csv')
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            Category.objects.get_or_create(
                name=row['name'],
                slug=row['slug'],
            )

    def import_genres(self, data_dir):
        """Import genres into database."""
        file_path = os.path.join(data_dir, 'genre.csv')
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            Genre.objects.get_or_create(
                name=row['name'],
                slug=row['slug'],
            )

    def import_titles(self, data_dir):
        """Import titles into database."""
        file_path = os.path.join(data_dir, 'titles.csv')
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            category = Category.objects.get(id=row['category'])
            Title.objects.get_or_create(
                name=row['name'],
                year=row['year'],
                category=category,
            )

    def import_genre_titles(self, data_dir):
        """Import genre title into database."""
        file_path = os.path.join(data_dir, 'genre_title.csv')
        df = pd.read_csv(file_path)
        for i, row in df.iterrows():
            title = Title.objects.get(id=row['title_id'])
            genre = Genre.objects.get(id=row['genre_id'])
            title.genres.add(genre)
            title.save()
