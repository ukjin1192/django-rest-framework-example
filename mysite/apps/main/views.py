#!usr/bin/python
# -*- coding:utf-8 -*-

from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import logout
from django.contrib.sessions.models import Session
from main.models import User, Article, Comment
from main.permissions import UserPermission, IsAuthorOrReadOnly
from main.serializers import UserSerializer, ArticleSerializer, CommentSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse


@api_view(['GET'])
@permission_classes((AllowAny, ))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'articles': reverse('article-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format)
    })


@api_view(['POST'])
@permission_classes((AllowAny, ))
def user_login(request):
    if all(x in request.data for x in ['email', 'password']):
        email = request.data['email']
        password = request.data['password']
    else:
        return Response(
                {'state': False, 'code': 1, 'message': 'Please put email and password to login.'},
                status=status.HTTP_200_OK)
    
    u = authenticate(email=email, password=password)
    
    if u:
        if u.is_active:
            login(request, u)
            return Response(
                    {'state': True, 'email': request.user.email, 'username': request.user.username}, 
                    status=status.HTTP_200_OK)
        else:
            return Response(
                    {'state': False, 'code': 2, 'message': 'Account is not active.'},
                    status=status.HTTP_200_OK)
    else:
        if User.objects.filter(email=email).count() > 0:
            return Response(
                    {'state': False, 'code': 3, 'message': 'Password is not correct.'},
                    status=status.HTTP_200_OK)
        else:
            return Response(
                    {'state': False, 'code': 4, 'message': 'Non existing email.'},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def user_logout(request):
    try:
        logout(request)
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ModelViewSet):
    """
    Provides `list`, `create`, `retrieve`, `update` and `destroy` actions for user object
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password=password, is_active=True)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        if 'password' in self.request.data:
            if 'original-password' not in self.request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if instance.check_password(self.request.data['original-password']) == False:
                return Response(
                        {'state': False, 'code': 1, 'message': 'Password is not correct.'},
                        status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        if 'is_active' in self.request.data and self.request.data['is_active'] == (False or 'false'):
            pass
            # TODO Delete token
        
        return Response(serializer.data)

    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
            # Authentication would be cleared after password changing
            u = authenticate(email=self.request.user.email, password=self.request.data['password'])
            login(self.request, u)
        else:
            serializer.save()


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
