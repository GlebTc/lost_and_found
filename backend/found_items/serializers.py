from rest_framework import serializers
from .models import FoundItem

class FoundItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoundItem
        fields = '__all__'  # Include all fields from the model
