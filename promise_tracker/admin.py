from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin, ExportMixin, ImportExportModelAdmin

# Register your models here.
from .models import Evidence, Promise, Politician, Party, Position, Rating, User

# class PartyValidityInline(admin.TabularInline):
#     model = PartyValidity
#     extra = 0

# region resourse
class PoliticianResource(resources.ModelResource):
    class Meta:
        model = Politician
class PromiseResource(resources.ModelResource):
    class Meta:
        model = Promise
class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_anonymous', 'created', 'updated')
class PartyResource(resources.ModelResource):
    class Meta:
        model = Party
class PositionResource(resources.ModelResource):
    class Meta:
        model = Position
class RatingResource(resources.ModelResource):
    class Meta:
        model = Rating
class EvidenceResource(resources.ModelResource):
    class Meta:
        model = Evidence
# endregion
class PoliticianAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_classes = [PoliticianResource]
    # inlines = [PartyValidityInline]    
    list_display = ('id', 'fname', 'lname', 'status')
    list_filter = ('party', 'status')


class PromiseAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_classes = [PromiseResource]
    # inlines = [PartyValidityInline]
    list_display = ('id', 'title', 'rating', 'politician', 'creator', 'date', 'status')
    list_filter = ('politician','politician__party','rating', 'status')

class PartyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PartyResource
    list_display = ('id', 'name', 'acronym')
    list_fiter = ('acronym',)
class EvidenceAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EvidenceResource
    list_display = ('id', 'title', 'source', 'promise', 'creator', 'status')
    list_fiter = ('promise', 'status')
    search_fields = ('title', 'creator')    
class PositionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PositionResource
class RatingAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = RatingResource
    list_display = ('title','description')
@admin.register(User)
class UserAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_class = UserResource
    list_display = ('id', 'username', 'email', 'is_anonymous', 'created', 'updated')
    list_filter = ('is_anonymous',)
    search_fields = ('username', 'email')

admin.site.register(Evidence, EvidenceAdmin)
admin.site.register(Promise, PromiseAdmin)
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(Party, PartyAdmin)
admin.site.register(Position, PositionAdmin)
admin.site.register(Rating, RatingAdmin)
# admin.site.register(User)
