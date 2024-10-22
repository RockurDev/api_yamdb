# Generated by Django 3.2 on 2024-10-21 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.SlugField(max_length=150, verbose_name='Слаг')),
                ('first_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Введите имя')),
                ('last_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Биография')),
                ('role', models.CharField(choices=[('anon', 'anonim'), ('admin', 'admin'), ('moderator', 'moderator'), ('user', 'user')], default='user', max_length=10, verbose_name='Роль')),
                ('confirmation_code', models.CharField(blank=True, editable=False, max_length=200, null=True, unique=True, verbose_name='Код подтверждения')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['username'],
                'abstract': False,
            },
        ),
        migrations.AddConstraint(
            model_name='customuser',
            constraint=models.UniqueConstraint(fields=('username', 'email'), name='unique_username_email'),
        ),
    ]
