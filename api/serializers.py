from rest_framework import serializers
from .models import HydroponicSystem, Measurement

class HydroponicSystemSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu HydroponicSystem.
    Pozwala na konwersję obiektów na JSON i odwrotnie.
    Pole `owner` jest tylko do odczytu i reprezentuje nazwę użytkownika.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'location', 'created_at', 'owner']


class MeasurementSerializer(serializers.ModelSerializer):
    """
    Serializer dla modelu Measurement.
    Konwertuje pomiary z czujników na format JSON.
    Pole `timestamp` jest tylko do odczytu, ponieważ generuje się automatycznie.
    """
    hydroponic_system = serializers.PrimaryKeyRelatedField(queryset=HydroponicSystem.objects.all())
    timestamp = serializers.ReadOnlyField()

    class Meta:
        model = Measurement
        fields = ['id', 'hydroponic_system', 'timestamp', 'ph', 'temperature', 'tds']
