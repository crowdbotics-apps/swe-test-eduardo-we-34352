from rest_framework import serializers
from apps.applications.models import App, Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = '__all__'

class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = '__all__'
        read_only_fields = ('screenshot', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        return App.objects.create(user=self.context['request'].user, **validated_data)

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        return Subscription.objects.create(user=self.context['request'].user, **validated_data)
