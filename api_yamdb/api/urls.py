from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, get_jwt_token, signup

from .views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)

v1_urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/signup/', signup, name='register'),
    path('auth/token/', get_jwt_token, name='token'),
]

urlpatterns = [
    path('v1/', include(v1_urlpatterns)),
]
