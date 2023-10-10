from django.contrib import admin

from .models import (Article, Author,
                    Category,Tag)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 
                    'content', 'pub_date',
                    )

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'bio')

@admin.register(Category)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Tag)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')