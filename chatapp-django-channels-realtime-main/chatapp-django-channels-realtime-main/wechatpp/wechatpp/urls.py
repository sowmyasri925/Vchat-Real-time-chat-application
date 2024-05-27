# urls.py in wechatpp project

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Importing auth views for logout
from chatapp import views  # Importing views from chatapp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),  # Registration view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
    path("accounts/", include("django.contrib.auth.urls")),  # Including auth URLs
    path('', include('chatapp.urls')),  # Including chatapp URLs
]
