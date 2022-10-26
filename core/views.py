from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.urls import reverse


def home_view(request):
    context = {"user_authenticated": False}
    if request.user.is_authenticated:
        context = {**context, "user_authenticated": True}
    return render(request, "home/index.html", context)


def login_view(request):
    context = {}
    if request.method == "GET":
        return render(request, "login/index.html", context)

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))

        else:
            return redirect("%s?next=%s" % (settings.LOGIN_URL, request.path))


def register_view(request):
    context = {}

    if request.method == "GET":
        return render(request, "register/index.html", context)

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.save()
        return render(request, "login/index.html", context)


def logout_view(request):
    context = {}
    logout(request)
    return render(request, "login/index.html", context)
