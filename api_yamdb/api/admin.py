from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'review', 'text')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'pub_date', 'score', 'text', 'title')
    search_fields = ('text', 'pub_date')
    list_filter = ('author', 'pub_date')


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'category', 'year')
    search_fields = ('name', 'description', 'year')
    list_filter = ('name', 'year', 'category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
