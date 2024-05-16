from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from .form import CustomUserLoginForm, CustomUserRegistrationForm


def custom_login(request):
    if request.method == "POST":
        print("POST REQUEST")
        print(request.POST["username"])
        form = CustomUserLoginForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if request.POST["username"] and request.POST["password"]:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                print("User is not None")
                messages.success(request, "You have successfully logged in.")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomUserLoginForm()
    return render(request, "users/Login.html", {"form": form})


def custom_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("login")


def custom_registration(request):
    if request.method == "POST":
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have successfully registered and logged in.")
            return redirect("dashboard")
    else:
        form = CustomUserRegistrationForm()
    return render(request, "users/register.html", {"form": form})
