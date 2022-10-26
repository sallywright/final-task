from django.urls import path
from . import views

app_name = "category"

urlpatterns = [
    path("create/", view=views.create_category_view, name="create"),
    path("list/", view=views.list_categories_view, name="list"),
    path("<int:category_id>/", view=views.get_category_view, name="view"),
]
