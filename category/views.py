from unicodedata import category
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import Http404
from utils import models
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
@require_http_methods(["GET", "POST"])
def create_category_view(request):
    context = {"user_authenticated": False}
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {**context, "user_authenticated": True}
            return render(request, "categories/create.html", context)
        else:
            return render(request, "login/index.html", context)
    if request.method == "POST":
        title = request.POST.get("title", None)
        user = request.user

        if title and user:
            try:
                category = models.Category(
                    title=title,
                    user=user,
                )
                category.full_clean()
                category.save()
                return redirect("category:list")
            except Exception as e:
                raise Http404(e)
        else:
            raise Http404("Invalid data")


@login_required
@require_http_methods(["GET"])
def list_categories_view(request):
    context = {"user_authenticated": False}
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {**context, "user_authenticated": True}
    categories = models.Category.objects.all()
    all_categories = []
    for category in categories:
        all_categories.append(
            {
                "id": category.id,
                "title": category.title,
                "notes": category.notes.filter(user=request.user),
            }
        )

    context = {**context, "categories": all_categories}
    if request.user.is_authenticated:
        context = {**context, "user_authenticated": True}
        return render(request, "categories/index.html", context)
    else:
        return render(request, "login/index.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def get_category_view(request, category_id):
    context = {"user_authenticated": False}
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                category = models.Category.objects.filter(id=category_id).first()
            except models.Category.DoesNotExist:
                raise Http404("Category does not exist")
            context = {
                **context,
                "user_authenticated": True,
                "category": category,
            }

            return render(request, "categories/view.html", context)
        else:
            return render(request, "login/index.html", context)


@login_required
@require_http_methods(["POST"])
def edit_category_view(request, category_id):
    context = {"user_authenticated": False}
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                category = (
                    models.Category.objects.filter(user=request.user)
                    .filter(id=category_id)
                    .first()
                )
            except models.Category.DoesNotExist:
                raise Http404("Category does not exist")

            category.title = request.POST.get("title", category.title)

            try:
                category.full_clean()
                category.save()
            except ValidationError as e:
                raise Http404(e)

            return redirect("category:list")
        else:
            return render(request, "login/index.html", context)


@login_required
@require_http_methods(["POST"])
def delete_category_view(request, category_id):
    context = {"user_authenticated": False}
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                category = models.Category.objects.filter(id=category_id).first()
            except models.Category.DoesNotExist:
                raise Http404("Category does not exist")

            category.delete()

            return redirect("category:list")
        else:
            return render(request, "login/index.html", context)
