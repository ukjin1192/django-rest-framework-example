#!usr/bin/python
# -*- coding:utf-8 -*-

from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password
from main.models import User, Article, Comment
from main.permissions import UserPermission, IsAuthorOrReadOnly
from main.serializers import UserSerializer, ArticleSerializer, CommentSerializer
from rest_framework import parsers, permissions, renderers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(['GET'])
@permission_classes((AllowAny, ))
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

    def create(self, request, *args, **kwargs):
        # Check captcha validation 
        if 'captcha-value' not in self.request.data or 'captcha-key' not in self.request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        captcha_key = self.request.data['captcha-key']
        captcha_value = self.request.data['captcha-value']
        
        try:
            captcha = CaptchaStore.objects.get(challenge=captcha_value, hashkey=captcha_key)
            captcha.delete()
        except:
            return Response(
                    {'state': False, 'code': 1, 'message': 'Captcha input is not correct.'},
                    status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password, is_active=True)

    # Note that update USERNAME_FIELD(=email) or password will refresh authentication token
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if 'email' in self.request.data or 'password' in self.request.data or 'is_active' in self.request.data:
            if 'original-password' not in self.request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if instance.check_password(self.request.data['original-password']) == False:
                return Response(
                        {'state': False, 'code': 1, 'message': 'Password is not correct.'},
                        status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update` and `destroy` actions for article object
    """
    queryset = Article.objects.select_related('author').prefetch_related('comments').filter(state='shown')
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update` and `destroy` actions for comment object
    """
    queryset = Comment.objects.select_related('author').select_related('article').filter(state='shown')
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, article_id=int(self.request.data['article_id']))


"""
Original source code to override methods

def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())

    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)

def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

def perform_create(self, serializer):
    serializer.save()

def retrieve(self, request, *args, **kwargs):
    instance = self.get_object()
    serializer = self.get_serializer(instance)
    return Response(serializer.data)

def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    return Response(serializer.data)

def perform_update(self, serializer):
    serializer.save()

def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    self.perform_destroy(instance)
    return Response(status=status.HTTP_204_NO_CONTENT)

def perform_destroy(self, instance):
    instance.delete()
"""
