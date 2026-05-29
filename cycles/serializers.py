from rest_framework import serializers
from .models import CycleTemplate, CyclePeriodDetail

class CyclePeriodDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CyclePeriodDetail
        fields = ['period_name', 'start_value', 'end_value', 'description', 'recommendations', 'color']

class CycleTemplateSerializer(serializers.ModelSerializer):
    period_details = CyclePeriodDetailSerializer(many=True, read_only=True)

    class Meta:
        model = CycleTemplate
        fields = ['name', 'cycle_type', 'description', 'period_details']
