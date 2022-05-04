from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("change_password/", views.change_password, name="change_password"),
    path("my_labels/", views.my_labels_view, name="my_labels"),
    path("my_labels/create/", views.create_my_label, name="create_my_label"),
]
