from rest_framework import serializers
from .models import *

class DepartmentSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Department
        fields = '__all__'

class CitySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    area = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = City
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    region = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Area
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    area = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Region
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='email', read_only=True)
    
    region = serializers.SlugRelatedField(slug_field='title', queryset=Region.objects.all())
    area = serializers.SlugRelatedField(slug_field='title', queryset=Area.objects.all())
    city = serializers.SlugRelatedField(slug_field='title', queryset=City.objects.all())
    department = serializers.SlugRelatedField(slug_field='title', queryset=Department.objects.all())

    class Meta:
        model = Ticket
        fields = '__all__'

class ActivateTicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = ('number', 'activation_code', 'status')