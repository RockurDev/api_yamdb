# Generated by Django 3.2 on 2024-10-29 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_comment_title_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='title_id',
            new_name='title',
        ),
    ]
