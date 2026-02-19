from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .forms import RegisterForms, UpdateProfileForm
from .forms import LoginForms




# Create your views here.
def register (request):
    if request.method == "GET":
        forms = RegisterForms()
        return render(request, "users/register.html", {"form": forms})                 
    if request.method == "POST":
        forms = RegisterForms(request.POST)
        if not forms.is_valid():
            return HttpResponse("Error")
        User.objects.create_user(
            username = forms.cleaned_data.get('username'),
            password = forms.cleaned_data.get("password"),


        )
        
    return redirect('/films/')

def login_user(request):

    if request.method == "GET":
        forms = LoginForms()
        return render(request, "users/login.html", {"forms": forms})

    if request.method == "POST":
        forms = LoginForms(request.POST)
        if not forms.is_valid():
            return HttpResponse("Error")
        user = authenticate(
            request, username=forms.cleaned_data.get("username"),
            password=forms.cleaned_data.get("password")
            
             )
        login(request,user)   
    return redirect ("/films/")

def logout_user(request):
    logout (request)
    return redirect("/")

def profile(request):
 
    return render(request, "users/profile.html")


def update_profile(request):
    if request.method == "GET":
        forms = UpdateProfileForm(request.POST or None)
        return render(request, "users/update_profile.html", context={"forms": forms})

    if request.method == "POST":
        forms = UpdateProfileForm(request.POST, request.FILES)
        if not forms.is_valid():
            return HttpResponse("Error")
        request.user.profile.age = forms.cleaned_data.get("age")
        request.user.profile.image = forms.cleaned_data.get("image")

        request.user.username = forms.cleaned_data.get("username")
        request.user.email = forms.cleaned_data.get("email")
        request.user.first_name = forms.cleaned_data.get("first_name")
        request.user.last_name = forms.cleaned_data.get("last_name")

        request.user.save()
        request.user.profile.save()

    return redirect("/films/")