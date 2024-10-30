from django.urls import path

from .views import get_jwt_token, signup

app_name = 'users'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('token/', get_jwt_token, name='token'),
]
