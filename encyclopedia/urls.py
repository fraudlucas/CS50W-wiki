from django.urls import path, re_path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^q", views.search, name="search"),
    path("random/page", views.random_entry, name="random"),
    path("add", views.add, name="add"),
    path("edit/<str:entry_title>", views.edit, name="edit"),
    path("<str:entry_title>", views.entry, name="entry"),
]
