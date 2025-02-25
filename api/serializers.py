from rest_framework import serializers
from .models import HydroponicSystem, Measurement

#Konwertowanie modelu HydroponicSystem
class HydroponicSystemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'location', 'created_at', 'owner']


#zapisywanie danych z czujników
class MeasurementSerializer(serializers.ModelSerializer):
    hydroponic_system = serializers.PrimaryKeyRelatedField(queryset=HydroponicSystem.objects.all())

    class Meta:
        model = Measurement
        fields = ['id', 'hydroponic_system', 'timestamp', 'ph', 'temperature', 'tds']
