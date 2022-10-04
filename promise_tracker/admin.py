from django.contrib import admin

# Register your models here.
from .models import Evidence, Promise, Politician, Party, PartyValidity, Position, Rating, Source, User

admin.site.register(Evidence)
admin.site.register(Promise)
admin.site.register(Politician)
admin.site.register(Party)
admin.site.register(PartyValidity)
admin.site.register(Position)
admin.site.register(Rating)
admin.site.register(Source)
admin.site.register(User)
