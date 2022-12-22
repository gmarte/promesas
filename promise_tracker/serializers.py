from rest_framework import serializers

from .models import Party, Promise, Politician

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('id', 'name','logo','acronym')
class PromiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promise
        fields = ('title','description', 'start_kpi', 'rating', 'politician', 'creator', 'date', 'status')
class PoliticianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politician    
        fields = '__all__'
