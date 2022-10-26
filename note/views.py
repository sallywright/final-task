from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.http import Http404
from utils import models
from django.views.decorators.http import require_http_methods
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
@require_http_methods(["GET", "POST"])
def create_note_view(request):
    context = {"user_authenticated": False}
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {**context, "user_authenticated": True}
            categories = models.Category.objects.all()
            context = {**context, "categories": categories}
            return render(request, "notes/create.html", context)
        else:
            return render(request, "login/index.html", context)
    if request.method == "POST":
        title = request.POST.get("title", None)
        text = request.POST.get("text", None)
        created_at = datetime.now()
        category_id = request.POST.get("category", None)
        if category_id:
            category = models.Category.objects.get(id=category_id)
        user = request.user
        picture_url = request.POST.get("image_url", None)

        if title and text and created_at and user:
            try:
                note = models.Note(
                    title=title,
                    text=text,
                    created_at=created_at,
                    category=category,
                    picture_url=picture_url,
                    user=user,
                )
                note.full_clean()
                note.save()
                return redirect("note:list")
            except Exception as e:
                raise Http404(e)
        else:
            raise Http404("Invalid data")


@login_required
@require_http_methods(["GET"])
def list_notes_view(request):
    context = {"user_authenticated": False}
    if request.method == "GET":
        if request.user.is_authenticated:
            context = {**context, "user_authenticated": True}

    if request.GET.get("search", None):
        search_string = request.GET.get("search")
        notes = models.Note.objects.filter(user=request.user).filter(
            title__icontains=search_string
        )
    else:
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
                "image_url": note.picture_url,
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
def get_note_view(request, note_id):
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
            categories = models.Category.objects.all()
            context = {
                **context,
                "user_authenticated": True,
                "note": notes,
                "categories": categories,
            }

            return render(request, "notes/view.html", context)
        else:
            return render(request, "login/index.html", context)


@login_required
@require_http_methods(["POST"])
def edit_note_view(request, note_id):
    context = {"user_authenticated": False}
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                note = (
                    models.Note.objects.filter(user=request.user)
                    .filter(id=note_id)
                    .first()
                )
            except models.Note.DoesNotExist:
                raise Http404("Note does not exist")

            note.title = request.POST.get("title", note.title)
            note.text = request.POST.get("text", note.text)
            category_id = request.POST.get("category", None)
            note.picture_url = request.POST.get("image_url", None)

            if category_id != None and category_id != "None" and category_id != "":
                note.category = models.Category.objects.get(id=category_id)
            try:
                note.full_clean()
                note.save()
            except ValidationError as e:
                raise Http404(e)

            return redirect("note:list")
        else:
            return render(request, "login/index.html", context)


@login_required
@require_http_methods(["POST"])
def delete_note_view(request, note_id):
    context = {"user_authenticated": False}
    if request.method == "POST":
        if request.user.is_authenticated:
            try:
                note = (
                    models.Note.objects.filter(user=request.user)
                    .filter(id=note_id)
                    .first()
                )
            except models.Note.DoesNotExist:
                raise Http404("Note does not exist")

            note.delete()

            return redirect("note:list")
        else:
            return render(request, "login/index.html", context)
