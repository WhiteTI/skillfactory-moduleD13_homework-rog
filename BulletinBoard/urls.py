"""
URL configuration for BulletinBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views

from BulletinBoard import settings
from ads import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ad/', views.ad_list, name='ad_list'),
    path('ad/create/', views.create_ad, name='create_ad'),
    path('ad/<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('ad/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ad/<int:ad_id>/review/create/', views.create_review, name='create_review'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/accept_review/<int:review_id>/', views.accept_review, name='accept_review'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
