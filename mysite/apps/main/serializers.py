#!usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from main.models import User, Article, Comment
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(many=True, view_name='article-detail', read_only=True)
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'email', 'username', 'password', 'is_active', 'date_joined', 'last_login', 'articles', 'comments')
        # Password would not display, but required when creating an object
        extra_kwargs = {'password': {'write_only': True}, }


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')
    comments = serializers.HyperlinkedRelatedField(many=True, view_name='comment-detail', read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('url', 'id', 'author', 'title', 'context', 'state', 'created_at', 'updated_at', 'comments', 'comments_count')

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    article = serializers.ReadOnlyField(source='article.title')
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = ('url', 'id', 'article', 'author', 'context', 'state', 'created_at', 'updated_at')
