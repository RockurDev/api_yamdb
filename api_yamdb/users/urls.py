from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_jwt_token, signup

app_name = 'users'

user_router = DefaultRouter()
user_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/token/', get_jwt_token, name='token'),
    path('auth/signup/', signup),
    path('', include(user_router.urls)),
]
