from django.urls import path

from .views import get_jwt_token, signup

app_name = 'users'

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', get_jwt_token, name='token'),
]
