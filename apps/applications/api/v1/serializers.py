from rest_framework import serializers
from apps.applications.models import App, Plan, Subscription

# Common serializer for created by
class CreatedBySerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def create(self, validated_data):
        return App.objects.create(created_by=self.context['request'].user, **validated_data)

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = '__all__'

class AppSerializer(CreatedBySerializer):

    class Meta:
        model = App
        fields = '__all__'
        read_only_fields = ('screenshot', 'created_by', 'created_at', 'updated_at')

class SubscriptionSerializer(CreatedBySerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('created_by', 'created_at', 'updated_at')
