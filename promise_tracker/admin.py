from django.contrib import admin
from import_export import resources
from import_export.admin import ImportMixin, ExportMixin, ImportExportModelAdmin

# Register your models here.
from .models import Evidence, Promise, Politician, Party, Position, Rating, Source, User

# class PartyValidityInline(admin.TabularInline):
#     model = PartyValidity
#     extra = 0
class PoliticianResource(resources.ModelResource):
    class Meta:
        model = Politician
class PoliticianAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_classes = [PoliticianResource]
    # inlines = [PartyValidityInline]    
    list_filter = ('party',)

class PromiseResource(resources.ModelResource):
    class Meta:
        model = Promise
class PromiseAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    resource_classes = [PromiseResource]
    # inlines = [PartyValidityInline]
    class Meta:
        model = Promise  
    list_filter = ('politician','rating')

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_anonymous', 'created', 'updated')
      
@admin.register(User)
class UserAdmin(ImportMixin, ExportMixin, admin.ModelAdmin):
    resource_class = UserResource
    list_display = ('id', 'username', 'email', 'is_anonymous', 'created', 'updated')
    list_filter = ('is_anonymous',)
    search_fields = ('username', 'email')

admin.site.register(Evidence)
admin.site.register(Promise, PromiseAdmin)
admin.site.register(Politician, PoliticianAdmin)
admin.site.register(Party)
admin.site.register(Position)
admin.site.register(Rating)
admin.site.register(Source)
# admin.site.register(User)
