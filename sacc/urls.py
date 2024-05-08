"""
URL configuration for sacc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include
from users.views import *
from home.views import *
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('',homepage,name="index"),
    path('dashboard/',dashboard,name="dashboard"),
    path('home/',homepage,name="home"),
    path('members',Members,name="members"),
    path('profile/',Profile,name="profile"),
    path('notifications/',notifications,name="notifications"),
    path('loans/',loans,name="loans"),
    path('transactions/',Transactions,name="transactions"),
    path('createuser/',CreateUser,name="createuser"),
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('register/', custom_registration, name='register'),
    path('member/<uuid:id>/', memberinfo, name="memberinfo"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)