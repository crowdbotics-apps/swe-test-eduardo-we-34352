from rest_framework import serializers
from apps.applications.models import App, Plan

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = '__all__'

class AppSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    def create(self, validated_data):
        return App.objects.create(created_by=self.context['request'].user, **validated_data)

    class Meta:
        model = App
        fields = '__all__'
        read_only_fields = ('screenshot', 'created_by', 'created_at', 'updated_at')
