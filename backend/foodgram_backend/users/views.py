from api.pagination import PageLimitPagination
from api.permissions import IsAuthorOrAdminOrReadOnly
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Follow, User
from users.serializers import CustomUserCreateSerializer, FollowSerializer


class CustomUserViewSet(UserViewSet):
    """Создание пользователя и подписка на него."""
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = PageLimitPagination

    @action(methods=['POST', 'DELETE', ],
            detail=True,)
    def subscribe(self, request, id):
        """Проверяет наличие подписки и создает/удаляет ее."""
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            if user == author:
                raise exceptions.ValidationError(
                    'На себя подписаться нельзя.')
            if Follow.objects.filter(user=user, author=author).exists():
                raise exceptions.ValidationError(
                    'Вы уже подписаны на данного автора.')
            serializer = FollowSerializer(
                author,
                request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if self.request.method == 'DELETE':
            if not Follow.objects.filter(user=user, author=author).exists():
                raise exceptions.ValidationError(
                    'Вы уже отписались от данного автора или '
                    'не были подписаны на него.')
            subscription = get_object_or_404(Follow, user=user, author=author)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FollowViewSet(viewsets.ReadOnlyModelViewSet):
    """Получение списка подписчиков."""
    serializer_class = FollowSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = PageLimitPagination

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)

    @action(methods=['GET', ],
            detail=False,)
    def subscribtions(self, request):
        """Получает подписки пользователя, сделавшего запрос."""
        if request.method == 'GET':
            user = request.user
            user_subscriptions = Follow.objects.filter(user=user)
            # authors = [user_sub.author.pk for user_sub in user_subscriptions]
            # authors_queryset = User.objects.filter(pk__in=authors)
            # page = self.paginate_queryset(authors_queryset)
            page = self.paginate_queryset(user_subscriptions)
            serializer = FollowSerializer(page, many=True,
                                          context={'request': request})
            # serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
