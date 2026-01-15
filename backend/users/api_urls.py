from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import RegisterAPIView, CurrentUserAPIView, LogoutAPIView

urlpatterns = [
    # JWT authentication
    path('login/', TokenObtainPairView.as_view(), name='api_login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    
    # User management
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('me/', CurrentUserAPIView.as_view(), name='api_current_user'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),
]