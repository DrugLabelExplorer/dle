from django.urls import path
from . import views
from dle import settings
from django.conf.urls.static import static

app_name = "users"

urlpatterns = [
    # url pattern referencing workflow of overall app
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('myqueries/', views.myqueries, name='myqueries'),

    path("profile/<int:userid>", views.profile, name="profile"),
    path("save_toggle/<int:postid>", views.save_toggle, name="save_toggle"),

    path("my_labels/", views.my_labels_view, name="my_labels"),
    path("my_labels/create/", views.create_my_label, name="create_my_label")


    # path("newitem", views.newitem, name="newitem"),
    # path("items/<int:item_id>", views.item, name="item"),
    # path("items/<int:item_id>/tracking", views.tracking, name="tracking"),
    # path("requested", views.requesteditem, name="requesteditem"),
    # path("requesteditem/add", views.requesteditem_add, name="requesteditem_add"),
    # path("requesteditem/delete", views.requesteditem_delete, name="requesteditem_delete")
]
