from django.urls import path
from . import api as user_apis
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', user_apis.RegisterView.as_view(), name='register'),
    path('login/', user_apis.UserLogin.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
