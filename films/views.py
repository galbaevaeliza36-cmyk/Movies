from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from films.forms import CreatFilmsForms
from films.models import Film, Category,Genre
from films.forms import SearchForm

# Create your views here.

@login_required(login_url="/login/")
def films_list(request):
    films = Film.objects.all()
    forms = SearchForm(request.GET or None) 

   
    search_query = request.GET.get("search", "")
    category_ids = request.GET.getlist("category_id")  # множественный выбор
    genre_ids = request.GET.getlist("genre_id")        # множественный выбор
    episodes_choice = request.GET.get("episodes_choice")

    
    if search_query:
        films = films.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    # Фильтр по категориям (множественный выбор)
    if category_ids:
        films = films.filter(category_id__in=category_ids)

    # Фильтр по жанрам (множественный выбор)
    if genre_ids:
        films = films.filter(genre__id__in=genre_ids).distinct()  

    # Фильтр по эпизодам
    if episodes_choice:
        if episodes_choice == "1":
            films = films.filter(episodes__gt=100)
        elif episodes_choice == "2":
            films = films.filter(episodes__lt=100)

    categories = Category.objects.all()
    genres = Genre.objects.all()

    context = {
        "films": films,
        "forms": forms,
        "categories": categories,
        "genres": genres,
        "selected_categories": list(map(int, category_ids)),
        "selected_genres": list(map(int, genre_ids)),
        "search_query": search_query,
        "episodes_choice": episodes_choice,
    }

    return render(request, "films/film_list.html", context)


   

def film_create(request):
    if request.method == 'GET':
        forms = CreatFilmsForms()
        return render(request, 'films/film_create.html')
    elif request.method == 'POST':
        forms = CreatFilmsForms(request.POST, request.FILES)
        print (forms)
        if forms.is_valid():
            Film.objects.create(
                title=forms.cleaned_data.get("title"),
                episodes=forms.cleaned_data.get('episodes'),
                image=forms.cleaned_data.get('image')
            )
            return redirect('/films/')
        

def base(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(
            request, 'base.html', context={'categories': categories, }
        )


def film_detail(request, film_id):
    if request.method == 'GET':
        film = Film.objects.get(id=film_id)
        return render(request, "films/film_detail.html", context={'film': film})

