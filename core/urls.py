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
from films.views import film_list, base, film_detail, film_create
from django.conf.urls import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('films/', film_list),
    path('films/<int:film_id>/', film_detail),
    path('', base),
    
    path('film_create/', film_create )
]+static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
