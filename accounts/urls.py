from django.urls import path
from accounts import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', views.RegisterApi.as_view(),name="register"),
    path('login/', views.LoginApi.as_view(),name="login"),
    path('profile/', views.ProfileApi.as_view(),name="profile"),
    path('token/refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
]