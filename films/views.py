from django.shortcuts import render, redirect
from films.models import Film, Category
# Create your views here.

def film_list(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id')
        films = Film.objects.all()
        if category_id:
            films = Film.objects.filter(category_id=category_id)
        return render(request, "films/film_list.html", context={"films": films})

def film_create(request):
    if request.method == 'GET':
        return render(request, 'films/film_create.html')
    elif request.method == 'POST':
        Film.objects.create(
            title=request.POST.get('title'),
            episodes=request.POST.get('episodes'),
            image=request.FILES.get('image')
        )
        return redirect('/films/')


def base(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        return render(request, 'base.html', context={'categories': categories})


def film_detail(request, film_id):
    if request.method == 'GET':
        film = Film.objects.get(id=film_id)
        return render(request, "films/film_detail.html", context={'film': film})

