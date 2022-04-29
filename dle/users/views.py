from django.shortcuts import render

# Create your views here.
import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.paginator import Paginator
# from .forms import CreateItemForm

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import User, MyQueries


def index(request):
    return render(request, "users/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            #    return HttpResponseRedirect(reverse("index"))
            return render(request, "users/index.html")

        else:
            return render(
                request,
                "users/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "users/login.html")


def logout_view(request):
    # returns user to login page
    logout(request)
    return HttpResponseRedirect(reverse("login"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "users/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "users/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        #    return HttpResponseRedirect(reverse("index"))
        return render(request, "users/index.html")
    else:
        return render(request, "users/register.html")


def change_password(request):
    if request.method == "POST":
        old_password = request.POST["old_password"]
        new_password = request.POST["new_password"]
        user = authenticate(request, username=request.user.username, password=old_password)
        if user is None:
            return render(
                request,
                "users/change_password.html",
                {"message": "Old password is incorrect."},
            )
        user.set_password(new_password)
        user.save()
        #    return HttpResponseRedirect(reverse("index"))
        return render(request, "users/index.html")
    else:
        return render(request, "users/change_password.html")



@login_required
def myqueries(request):
    request.user 
    return render(request, "users/myqueries.html")

# save the query to user's queries
@login_required
def savequery(request):
    if request.method == "POST":
        query = request.POST["query"]
        results = request.POST["results"]
        user = request.user
        myquery = MyQueries(user=user, query=query, results=results)
        myquery.save()
        return render(request, "users/myqueries.html")
    else:
        return render(request, "users/myqueries.html")


@login_required(login_url='login')
# user can view any user profile according to specs
def profile(request, userid):
    allpost = User.objects.get(
        pk=userid).posts_created.order_by('-timestamp').all()
    paginator = Paginator(allpost, 10)
    page = request.GET.get('page')

    return render(request, "network/profile.html", {
        "viewed_user": User.objects.get(pk=userid),
        "allposts": paginator.get_page(page)
    })        