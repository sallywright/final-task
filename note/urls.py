from django.urls import path
from . import views

app_name = "note"

urlpatterns = [
    path("create/", view=views.create_note_view, name="create"),
    path("list/", view=views.list_notes_view, name="list"),
    path("<int:note_id>/", view=views.get_note_view, name="view"),
    path("<int:note_id>/edit/", view=views.edit_note_view, name="edit"),
    path("<int:note_id>/delete/", view=views.delete_note_view, name="delete"),
]
