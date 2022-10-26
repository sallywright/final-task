from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("note/", include("note.urls")),
    path("category/", include("category.urls")),
]
