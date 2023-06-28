from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)
from . import views

urlpatterns = [
    path('user/register/', views.Register.as_view(), name='user-register'),
    path('user/login/', TokenObtainPairView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token-blacklist'),
    path('user/<uuid:pk>', views.UserView.as_view(), name='user-detail'),
    path('user/', views.CurrentUser.as_view(), name='current-user-detail')
]
