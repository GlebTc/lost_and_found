from rest_framework import serializers
from .models import Site, Building, Level, Department

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            'id': rep['id'],
            'name': rep['name'],
            'level': rep['level']
        }

class LevelSerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Level
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            'id': rep['id'],
            'name': rep['name'],
            'building': rep['building'],
            'departments': rep['departments']
        }

class BuildingSerializer(serializers.ModelSerializer):
    levels = LevelSerializer(many=True, read_only=True)

    class Meta:
        model = Building
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            'id': rep['id'],
            'name': rep['name'],
            'site': rep['site'],
            'levels': rep['levels']
        }

class SiteSerializer(serializers.ModelSerializer):
    buildings = BuildingSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return {
            'id': rep['id'],
            'name': rep['name'],
            'buildings': rep['buildings']
        }
