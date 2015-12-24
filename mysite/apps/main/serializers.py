#!usr/bin/python
# -*- coding: utf-8 -*-

from main.models import User, Article, Comment
from rest_framework import serializers
from rest_framework.settings import api_settings


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
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('url', 'id', 'author', 'title', 'context', 'state', 'created_at', 'updated_at', 'comments', 'comments_count')

    def get_comments(self, obj):
        """
        Get paginated comments
        """
        comments = Comment.objects.select_related('author').select_related('article').\
                filter(article=obj, state='shown')[:api_settings.PAGE_SIZE]
        serializer = CommentSerializer(comments, many=True, context={'request': self.context['request']})
        return serializer.data

    def get_comments_count(self, obj):
        """
        Get number of comments in specific article
        """
        return obj.comments.count()


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    author_email = serializers.ReadOnlyField(source='author.email')
    author_username = serializers.ReadOnlyField(source='author.username')
    article = serializers.ReadOnlyField(source='article.title')

    class Meta:
        model = Comment
        fields = ('url', 'id', 'article', 'author_email', 'author_username', 'context', 'state', 'created_at', 'updated_at')
