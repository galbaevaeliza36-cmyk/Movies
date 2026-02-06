from django.contrib import admin
from films.models import Film, Category, Genre
# Register your models here.

admin.site.register(Film)
admin.site.register(Category)
admin.site.register(Genre)
