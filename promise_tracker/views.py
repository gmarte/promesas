
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import Promise, Evidence, Party, Position, Politician, Source, User


def index(request):
    un_filtered = ''
    paginator = Paginator(un_filtered, 10)  # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "promise_tracker/index.html", {
        "posts": page_obj,
    })


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
            return render(request, "promise_tracker/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "promise_tracker/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "promise_tracker/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "promise_tracker/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "promise_tracker/register.html")


""" MODEL APP VIEWS"""


class PromiseBaseView(View):
    model = Promise
    fields = '__all__'
    success_url = reverse_lazy('promise:index')


class PromiseListView(PromiseBaseView, ListView):
    """View to list all pipromise.
    Use the 'promise_list' variable in the template
    to access all Promise objects"""


class PromiseCreateView(PromiseBaseView, CreateView):
    template_name = 'promise/promise_form.html'
    """View to create a new promise"""


class PositionBaseView(View):
    model = Position
    fields = ['name']
    success_url = reverse_lazy('positions')


class PositionListView(PositionBaseView, ListView):
    template_name = 'position/position_list.html'
    """View to list all Positions.
    Use the 'Position_list' variable in the template
    to access all Position objects"""


class PositionDetailView(PositionBaseView, DetailView):
    """View to list the details from one Position.
    Use the 'Position' variable in the template to access
    the specific Position here and in the Views below"""


class PositionCreateView(PositionBaseView, CreateView):
    template_name = 'position/position_form.html'
    # template_name = 'position/position_form.html'


class PositionUpdateView(PositionBaseView, UpdateView):
    """View to update a Position"""


class PositionDeleteView(PositionBaseView, DeleteView):
    """View to delete a Position"""
