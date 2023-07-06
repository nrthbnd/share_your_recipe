from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, FollowViewSet

app_name = 'users'

router = DefaultRouter()

router.register(
    'users/subscriptions',
    FollowViewSet,
    basename='subscriptions')

router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
