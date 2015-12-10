#!usr/bin/python
# -*- coding:utf-8 -*-

from django.contrib.auth.hashers import make_password
from main.models import User, Article, Comment
from main.permissions import UserPermission, IsAuthorOrReadOnly
from main.serializers import UserSerializer, ArticleSerializer, CommentSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'articles': reverse('article-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format)
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update` and `destroy` actions for user object
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password)

    # Partial update also executes perform_update
    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    @detail_route(methods=['POST'], url_path='change-password')
    def change_password(self, request, pk=None):
        if all(x in request.data for x in ['original-password', 'new-password']):
            user = self.get_object()
            if user.check_password(request.data['original-password']):
                user.set_password(request.data['new-password'])
                user.save()
                return Response(user, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class ArticleViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update` and `destroy` actions for article object
    """
    queryset = Article.objects.filter(state='shown')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update` and `destroy` actions for comment object
    """
    queryset = Comment.objects.filter(state='shown')
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, article_id=int(self.request.data['article_id']))
