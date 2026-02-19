"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path
from films.views import films_list, base, film_detail, film_create
from django.conf.urls import static
from django.conf import settings
from films import views

from users.views import register,profile, login_user, logout_user,update_profile
users = [
    path("register/", register),
    path("login/", login_user),
    path("logout/",logout_user , name="logout"),
    path("profile/",profile),
    path("update_profile/", update_profile),

]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('films/', films_list, name='films_list'), 
    path('add/', views.add_film, name='add_film'),  
    path('films/<int:film_id>/', film_detail, name='film_detail'),  
    path('', base, name='base'),
    path('film_create/', film_create, name='film_create'),
    *users
] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

