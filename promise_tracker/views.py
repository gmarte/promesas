## CBV
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
## Viewsets / REST Framework
from promise_tracker.serializers import PromiseSerializer, PartySerializer, PoliticianSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Count
from django.db.models import Q
#from django.http import JsonResponse
#import json

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
#from django.core.paginator import Paginator
from PIL import Image
from django.forms import inlineformset_factory
from promise_tracker.forms import PromisesForm
from promise_tracker.forms import EvidenceForm

from .models import Promise, Evidence, Party, Position, Politician, Source, User, PartyValidity, Rating


def index(request):
    
    promises = Promise.objects.all()
    politicians = Politician.objects.all()
    politicians_count = Politician.objects.all().count()
    evidences_count = Evidence.objects.filter(status=True).count()
    parties = Party.objects.all()
    parties_count = Party.objects.all().count()
    promises_count = Promise.objects.filter(status=True).count()
   
    return render(request, "promise_tracker/index.html", {
        "promises": promises,
        "promises_count": promises_count,
        "politicians": politicians,
        "politicians_count": politicians_count,
        "parties": parties,
        "parties_count": parties_count,
        "evidences_count": evidences_count,
        "segment": 'index'
    })

# region User
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
# endregion

#region Promise
class PromiseBaseView(View):
    model = Promise
    # fields = ['title','description', 'politician', 'start_kpi', 'rating']    
    form_class = PromisesForm
    success_url = reverse_lazy('index')


class PromiseListView(PromiseBaseView, ListView):
    template_name = 'promise/promise_list.html'
    """View to list all pipromise.
    Use the 'promise_list' variable in the template
    to access all Promise objects"""


class PromiseCreateView(PromiseBaseView, CreateView):
    template_name = 'promise/promise_form.html'
    """View to create a new promise"""
    def get_context_data(self, **kwargs):                
        # source_form = source.get_form_class()
        formset = EvidenceForm
        context = super().get_context_data(**kwargs)
        context['formset'] = formset        
        return context        

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        promise_evidence_form = EvidenceForm(self.request.POST)
        if form.is_valid() and promise_evidence_form.is_valid():
            return self.form_valid(form, promise_evidence_form)
        else:
            return self.form_invalid(form, promise_evidence_form)
    def form_valid(self, form, promise_evidence_form):
        form.instance.creator_id = self.request.user.id        
        self.object = form.save()                

        # saving Evidence Instances
        evidence = promise_evidence_form.save(commit=False)
        evidence.creator = self.request.user
        evidence.promise = self.object
        evidence.save()
        # for sc in source:                        
        #     sc.save()

        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form, promise_evidence_form):        
        return self.render_to_response(
                 self.get_context_data(form=form,
                                       formset=promise_evidence_form
                                       )
        )
class PromiseDetailView(PromiseBaseView, DetailView):
    template_name = 'promise/promise_detail.html'
    
    """View to list the details from one Promise.
    Use the 'Promise' variable in the template to access
    the specific Promise here and in the Views below"""   
    def get_context_data(self, **kwargs):    
        formset = EvidenceForm                
        self.object = self.get_object()    
        evidences = self.object.evidences.all()
        context = super().get_context_data(**kwargs)
        context['evidences'] = evidences      
        context['formset'] = formset         
        return context 

class PromiseUpdateView(PromiseBaseView, UpdateView):
    template_name = 'promise/promise_form.html'
    """View to update a Promise"""


class PromiseDeleteView(PromiseBaseView, DeleteView):
    template_name = 'promise/promise_confirm_delete.html'
    """View to delete a Promise"""    
class PromiseViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Promise.objects.all()
    serializer_class = PromiseSerializer

    @action(detail=False, methods=['get'], url_path='party')
    def promises_parties(self, request, *args, **kwargs):
        data = []
        datap = {}
        ratings = []                
        partyId = request.query_params.get('id')
        if not partyId:        
            parties = Party.objects.all()
            for p in parties:
                data.append(
                    {
                        'id': p.id,
                        'party': p.acronym,
                        'count': Promise.objects.filter(politician__party=p, status=True).count()
                    }
                )
            return Response(data, status=status.HTTP_200_OK)
        else:
            singleParty = Party.objects.get(pk=partyId)
            party_serialize = PartySerializer(singleParty)
            # Transaction.objects.all().values('actor').annotate(total=Count('actor')).order_by('total')
            rating_by_party = Count('ratings', filter=Q(ratings__politician__party = singleParty))
            ratingsParty = Rating.objects.annotate(number_of_ratings = rating_by_party)            
            datap = party_serialize.data
            for r in ratingsParty:
                ratings.append(
                    {
                        'title': r.title,
                        'count': r.number_of_ratings
                    }
                )
            datap["ratings"] = ratings
            return Response(datap, status=status.HTTP_200_OK)
        # return Response(data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='politician')
    def promises_politician(self, request, *args, **kwargs):
        data = []
        datap = {}
        ratings = [] 
        politicianId = request.query_params.get('id')
        if not politicianId:
            politician = Politician.objects.all()        
            for p in politician:
                if p.promise_count > 0:
                    data.append(
                        {
                            'id' : p.id,
                            'party': p.party.acronym,
                            'name': p.fname + ' ' + p.lname,                    
                            'count': p.promise_count
                        }
                    )
            return Response(data, status=status.HTTP_200_OK)
        else:
            singlePolitician = Politician.objects.get(pk=politicianId)
            politician_serialize = PoliticianSerializer(singlePolitician)
            rating_by_politican = Count('ratings', filter=Q(ratings__politician = singlePolitician))
            ratingsPolitician = Rating.objects.annotate(number_of_ratings = rating_by_politican)            
            datap = politician_serialize.data
            for r in ratingsPolitician:
                ratings.append(
                    {
                        'title': r.title,
                        'count': r.number_of_ratings
                    }
                )
            datap["ratings"] = ratings
            return Response(datap, status=status.HTTP_200_OK)



#endregion

# region Position
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
# endregion

# region Parties
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
# endregion

#region Politician
class PoliticianBaseView(View):
    model = Politician
    fields = ['fname','lname','country', 'party','religion', 'education','photo','position']
    labels = {'fname':'First Name:'}
    # PoliticianPartyFormSet = inlineformset_factory(Politician, PartyValidity, fields=('party', 'ini', 'end'))
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
        # formset = self.PoliticianPartyFormSet(queryset=Politician.objects.none())
        context = super().get_context_data(**kwargs)
        # context['formset'] = formset        
        return context        

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        # politician_validity_form = self.PoliticianPartyFormSet(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        form.instance.creator_id = self.request.user.id        
        self.object = form.save()                

        # saving Party Validity Instances
        # party_validity = politician_validity_form.save(commit=False)
        # for pv in party_validity:    
        #     pv.politician = self.object        
        #     pv.save()

        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form):        
        return self.render_to_response(
                 self.get_context_data(form=form)
        )


class PoliticianUpdateView(PoliticianBaseView, UpdateView):
    template_name = 'politician/politician_form.html'
    """View to update a Politician"""
    def get_context_data(self, **kwargs):        
        self.object = self.get_object()
        # formset = self.PoliticianPartyFormSet(instance=self.object)
        context = super().get_context_data(**kwargs)
        # context['formset'] = formset        
        return context 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)       
        # politician_validity_form = self.PoliticianPartyFormSet(self.request.POST, instance=self.object)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    def form_valid(self, form):
        # form.instance.creator_id = self.request.user.id        
        self.object = form.save()                

        # saving Party Validity Instances
        # party_validity = politician_validity_form.save(commit=False)
        # for pv in party_validity:    
        #     pv.politician = self.object        
        #     pv.save()

        return HttpResponseRedirect(self.get_success_url())
    def form_invalid(self, form, politician_validity_form):        
        return self.render_to_response(
                 self.get_context_data(form=form)
        )

class PoliticianDeleteView(PoliticianBaseView, DeleteView):
    template_name = 'politician/politician_confirm_delete.html'
    """View to delete a Politician"""
# endregion