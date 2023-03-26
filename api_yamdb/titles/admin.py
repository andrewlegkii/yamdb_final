from django.contrib import admin

from .models import Category, Genre, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])

    get_genres.short_description = 'Жанр'
    list_display = ('id', 'name', 'year', 'category', 'get_genres', 'rating')
    search_fields = ('name', 'year')
    list_filter = ('year', 'genre', 'category', 'rating')
    empty_value_display = '-пусто-'
    exclude = ('rating',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
