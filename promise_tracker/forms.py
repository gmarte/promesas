from django import forms
from django.forms import inlineformset_factory
from .models import Promise, Evidence, Party, Position, Politician, Source, User, PartyValidity, Rating

class PromisesForm(forms.ModelForm):
    title = forms.CharField(label='Title:', max_length=200, widget=forms.TextInput(
                              attrs={'class': 'form-control'}))
    description = forms.CharField(label='Description:', widget=forms.Textarea(
                              attrs={'class': "form-control"}))                           
    politician = forms.ModelChoiceField(label='Politician:', widget=forms.Select(attrs={'class': "form-control"}), queryset=Politician.objects.filter(status=True))  
    start_kpi = forms.CharField(label='Key performance indicator (KPI):', widget=forms.TextInput(attrs={'class': "form-control"}))                              
    rating = forms.ModelChoiceField(label='Rating:', widget=forms.Select(attrs={'class': "form-control"}),queryset=Rating.objects.all())
    
    class Meta:
        model = Promise
        fields = ['title','description', 'fuentes', 'politician', 'start_kpi', 'rating']
        # widget = {
        # 'title': forms.TextInput(attrs={'class':'form-control'}),
        # }

    # fuentes = models.ManyToManyField(Source, related_name="promise_sources")
    # creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)
    # date = models.DateField(auto_now_add=True)
    # status = models.BooleanField(default=False)
class SourceForm(forms.ModelForm):
    NEWS = '01'
    VIDEO = '02'
    PHOTO = '03'
    TYPES_CHOICES = [
        (NEWS, 'Prensa'),
        (VIDEO, 'Video'),
        (PHOTO, 'Foto'),
    ]
    title = forms.CharField(label='Title:', max_length=200, widget=forms.TextInput(
                              attrs={'class': 'form-control'}))
    type = forms.ChoiceField(label='Type', widget=forms.Select(attrs={'class': 'form-control'}), choices=TYPES_CHOICES)  
    class Meta:
        model = Source
        fields = ['title', 'type']