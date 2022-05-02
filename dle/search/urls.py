from django.urls import path

from . import views

app_name = "search"

urlpatterns = [
    path("", views.index, name="index"),
    path("results", views.list_search_results, name="list_search_results"),
    path("<int:drug_id>", views.view_drug, name="view_drug")
]
