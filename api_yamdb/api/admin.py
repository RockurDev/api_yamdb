from django.contrib import admin

from .models import Genre


class GenreAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	search_fields = ('name', 'slug')
	list_editable = ('name', 'slug')


admin.site.register(Genre, GenreAdmin)
