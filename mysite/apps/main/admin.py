#!usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from main.models import User, Article, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'is_active')
    search_fields = ('email', 'username')
    list_filter = ('last_login', )
    date_hierarchy = 'last_login'
    ordering = ('-id', )

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'hits', 'state')
    search_fields = ('title',)
    list_filter = ('created_at', )
    date_hierarchy = 'created_at'
    ordering = ('-id', )

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'state')
    list_filter = ('created_at', )
    date_hierarchy = 'created_at'
    ordering = ('-id', )


admin.site.register(User, UserAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
