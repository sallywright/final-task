from unicodedata import category
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
            return render(request, "notes/create.html", context)
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
    notes = models.Note.objects.filter(user=request.user)
    all_notes = []
    for note in notes:
        all_notes.append(
            {
                "id": note.id,
                "title": note.title,
                "text": note.text,
                "created_at": note.created_at,
                "category": note.category,
            }
        )

    context = {**context, "notes": notes}
    if request.user.is_authenticated:
        context = {**context, "user_authenticated": True}
        return render(request, "notes/index.html", context)
    else:
        return render(request, "login/index.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def get_category_view(request, note_id):
    context = {"user_authenticated": False}
    if request.method == "GET":
        if request.user.is_authenticated:
            try:
                notes = (
                    models.Note.objects.filter(user=request.user)
                    .filter(id=note_id)
                    .first()
                )
            except models.Note.DoesNotExist:
                raise Http404("Note does not exist")
            context = {
                **context,
                "user_authenticated": True,
                "note": notes,
            }

            return render(request, "notes/view.html", context)
        else:
            return render(request, "login/index.html", context)
