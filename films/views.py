import math
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from films.forms import CreatFilmsForms
from django.views.generic import CreateView, ListView, DeleteView,DetailView,TemplateView
from films.models import Film, Category,Genre
from films.forms import SearchForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden



class FilmListView(LoginRequiredMixin, ListView):
    model = Film
    template_name = "films/film_list.html"
    context_object_name = "films"
    paginate_by = 3
    login_url = "/login/"

    def get_queryset(self):
        queryset = Film.objects.all()

        search_query = self.request.GET.get("search", "")
        category_ids = self.request.GET.getlist("category_id")
        genre_ids = self.request.GET.getlist("genre_id")
        episodes_choice = self.request.GET.get("episodes_choice")

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        if category_ids:
            queryset = queryset.filter(category_id__in=category_ids)

        if genre_ids:
            queryset = queryset.filter(genre__id__in=genre_ids).distinct()

        if episodes_choice:
            if episodes_choice == "1":
                queryset = queryset.filter(episodes__gt=100)
            elif episodes_choice == "2":
                queryset = queryset.filter(episodes__lt=100)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["forms"] = SearchForm(self.request.GET or None)
        context["categories"] = Category.objects.all()
        context["genres"] = Genre.objects.all()

        context["selected_categories"] = list(
            map(int, self.request.GET.getlist("category_id"))
        )
        context["selected_genres"] = list(
            map(int, self.request.GET.getlist("genre_id"))
        )
        context["search_query"] = self.request.GET.get("search", "")
        context["episodes_choice"] = self.request.GET.get("episodes_choice")

        return context


# def film_create(request):
#     user = request.user
#     if user.is_staff:
#         if request.method == 'GET':
#             form = CreatFilmsForms()
#             return render(request, 'films/film_create.html', {'form': form})

#         elif request.method == 'POST':
#             form = CreatFilmsForms(request.POST, request.FILES)  
#             if form.is_valid():
#                 Film.objects.create(
#                     title=form.cleaned_data.get("title"),
#                     episodes=form.cleaned_data.get("episodes"),
#                     image=form.cleaned_data.get("image")
#                 )
#                 return redirect('/films/')
#         else:
#                 return render(request, 'films/film_create.html', {'form': form})
#         return HttpResponse ("Error")
#     return HttpResponse("Permission denied" )



class FilmCreateView(LoginRequiredMixin, CreateView):
    model = Film
    form_class = CreatFilmsForms
    template_name = "films/film_create.html"
    success_url = reverse_lazy("films_list")

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)
   

class FilmDeleteView(LoginRequiredMixin, DeleteView):
    model = Film
    success_url = reverse_lazy("films_list")

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.profile != request.user.profile:
            return HttpResponseForbidden("Permission denied")
        return super().dispatch(request, *args, **kwargs)

class BaseView(TemplateView):
    template_name = "base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class FilmDetailView(DetailView):
    model = Film
    template_name = "films/film_detail.html"
    context_object_name = "film"
    pk_url_kwarg = "film_id"
