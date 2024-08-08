from django.urls import path
from user_accounts.views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/users/register", RegisterView.as_view(), name="register"),
    path("api/v1/users/login", LoginView.as_view(), name="login"),
]
