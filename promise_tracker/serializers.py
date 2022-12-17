from rest_framework import serializers

from .models import Party, Promise, Politician

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ('id', 'name','logo','acronym')
class PromiseSerializar(serializers.ModelSerializer):
    class Meta:
        model = Promise
class PoliticianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Politician        
