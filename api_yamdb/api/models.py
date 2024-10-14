from django.db import models


class Genre(models.Model):
	"""Класс реализующий модель Жанра."""
	name = models.CharField(
		max_length=256,
		on_delete=models.SET_NULL,
		verbose_name='Название'
	)
	slug = models.SlugField(
		max_length=50,
		unique=True,
		verbose_name='Слаг'
	)

	class Meta:
		verbose_name = 'Жанр'
		verbose_name_plural = 'Жанры'
	
	def __str__(self):
		return self.name
