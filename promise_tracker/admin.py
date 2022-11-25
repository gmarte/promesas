from django.contrib import admin

# Register your models here.
from .models import Evidence, Promise, Politician, Party, PartyValidity, Position, Rating, Source, User

class PartyValidityInline(admin.TabularInline):
    model = PartyValidity
    entra = 0
class PoliticianAdmin(admin.ModelAdmin):
    inlines = [PartyValidityInline]
    class Meta:
        model = Politician


admin.site.register(Evidence)
admin.site.register(Promise)
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(Party)
admin.site.register(PartyValidity)
admin.site.register(Position)
admin.site.register(Rating)
admin.site.register(Source)
admin.site.register(User)
