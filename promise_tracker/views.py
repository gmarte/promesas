
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
from PIL import Image
from django.forms import inlineformset_factory

# from .models import *
from .models import Promise, Evidence, Party, Position, Politician, Source, User, PartyValidity


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

### Position

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
    template_name = 'position/position_detail.html'
    
    """View to list the details from one Position.
    Use the 'Position' variable in the template to access
    the specific Position here and in the Views below"""


class PositionCreateView(PositionBaseView, CreateView):
    template_name = 'position/position_form.html'
    # template_name = 'position/position_form.html'


class PositionUpdateView(PositionBaseView, UpdateView):
    template_name = 'position/position_form.html'
    """View to update a Position"""


class PositionDeleteView(PositionBaseView, DeleteView):
    template_name = 'position/position_confirm_delete.html'
    """View to delete a Position"""

### Parties


class PartyBaseView(View):
    model = Party
    fields = '__all__'
    success_url = reverse_lazy('parties')


class PartyListView(PartyBaseView, ListView):
    template_name = 'party/party_list.html'
    """View to list all Partys.
    Use the 'Party_list' variable in the template
    to access all Party objects"""


class PartyDetailView(PartyBaseView, DetailView):
    template_name = 'party/party_detail.html'
    
    """View to list the details from one Party.
    Use the 'Party' variable in the template to access
    the specific Party here and in the Views below"""


class PartyCreateView(PartyBaseView, CreateView):
    template_name = 'party/party_form.html'
    # template_name = 'Party/Party_form.html'
    # def post(self, request, *args, **kwargs):
    #     form = self.form_class(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()


class PartyUpdateView(PartyBaseView, UpdateView):
    template_name = 'party/party_form.html'
    """View to update a Party"""
    # def post(self, request, *args, **kwargs):
    #     print(request.FILES)
    #     return super().post(self,request, *args, **kwargs)
    # def form_valid(self, form):
    #     print(form.cleaned_data)
    #     return super().form_valid(form)
            


class PartyDeleteView(PartyBaseView, DeleteView):
    template_name = 'party/party_confirm_delete.html'
    """View to delete a Party"""


class PoliticianBaseView(View):
    model = Politician
    fields = ['fname','lname','country','religion', 'education','photo','position']
    success_url = reverse_lazy('politicians')    


class PoliticianListView(PoliticianBaseView, ListView):
    template_name = 'politician/politician_list.html'
    """View to list all Politicians.
    Use the 'politician_list' variable in the template
    to access all Politician objects"""


class PoliticianDetailView(PoliticianBaseView, DetailView):
    template_name = 'politician/politician_detail.html'
    
    """View to list the details from one Politician.
    Use the 'Politician' variable in the template to access
    the specific Politician here and in the Views below"""


class PoliticianCreateView(PoliticianBaseView, CreateView):
    template_name = 'politician/politician_form.html'    
    # def get(request, *args, **kwargs):        
    #     # context = {'context' : formset}
    def get_context_data(self, **kwargs):
        OrderFormSet = inlineformset_factory(Politician, PartyValidity, fields=('party', 'ini', 'end'))
        formset = OrderFormSet(queryset=Politician.objects.none())
        context = super().get_context_data(**kwargs)
        context['formset'] = formset        
        return context        

    def form_valid(self, form):
        print(form)
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PoliticianUpdateView(PoliticianBaseView, UpdateView):
    template_name = 'politician/politician_form.html'
    """View to update a Politician"""


class PoliticianDeleteView(PoliticianBaseView, DeleteView):
    template_name = 'politician/politician_confirm_delete.html'
    """View to delete a Politician"""
