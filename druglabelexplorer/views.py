import decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import CreateItemForm

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import Tracking, Item, User



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "druglabelexplorer/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "druglabelexplorer/login.html")


def logout_view(request):
    #returns user to login page
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
            return render(request, "druglabelexplorer/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "druglabelexplorer/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "druglabelexplorer/register.html")


@login_required
def tracking(request, item_id):
    #once user is logged in, they would have access to update track history
    if request.method == "POST":
        content = request.POST["tracking"]
        tracking = Tracking(tracker=request.user, content=content, item=item)
        item = get_object_or_404(Item, pk=item_id)
        tracking.save()
        return HttpResponseRedirect(reverse("item", args=(item.id,)))


def newitem(request):
    #function to submit new item 
    if request.method == "POST":
        form = CreateItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.contributor = request.user
            form.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "druglabelexplorer/newitem.html", {
                "form": form
            })
    else:
        return render(request, "druglabelexplorer/newitem.html", {
            "form": CreateItemForm()
        })


def index(request):
    #function showing all item cards on index.html in reverse chronological order
    items = Item.objects.filter(active=True).order_by("-timeadded").all()
    return render(request, "druglabelexplorer/index.html", {
        "title": "Active Items",
        "items": items
    })


def item(request, item_id):
    
    item = get_object_or_404(Item, pk=item_id)
    on_requesteditem = request.user.is_authenticated and (
        item in request.user.requesteditem.all())
    return render(request, "druglabelexplorer/itemprofile.html", {
        "trackings": item.trackings.order_by("-timeadded").all(),
        "item": item,
        "on_requesteditem": on_requesteditem
    })


@login_required
def requesteditem(request):
   
    items = request.user.requesteditem.order_by("-timeadded").all()
    return render(request, "druglabelexplorer/index.html", {
        "title": "Requesteditem",
        "items": items
    })


@login_required
def requesteditem_add(request):
   
    if request.method == "POST":
        item = get_object_or_404(Item, pk=int(request.POST["item_id"]))
        request.user.requesteditem.add(item)
        return HttpResponseRedirect(reverse("item", args=(item.id,)))


@login_required
def requesteditem_delete(request):
   
    if request.method == "POST":
        item = get_object_or_404(Item, pk=int(request.POST["item_id"]))
        request.user.requesteditem.remove(item)
        return HttpResponseRedirect(reverse("item", args=(item.id,)))
