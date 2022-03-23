from rest_framework import serializers
from apps.applications.models import App, Plan, Subscription

class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = ('id', 'name', 'description', 'price', 'created_at', 'updated_at')

class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ('id', 'name', 'description', 'type', 'framework', 'domain_name', 'screenshot', 'subscription', 'user', 'created_at', 'updated_at')
        read_only_fields = ('subscription', 'screenshot', 'user', 'created_at', 'updated_at')

    def create(self, validated_data):
        return App.objects.create(user=self.context['request'].user, **validated_data)

class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'plan', 'app', 'active', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')
        extra_kwargs = {
            'plan': {'required': True},
            'app': {'required': True},
        }

    def create(self, validated_data):
        app = validated_data.get('app')
        if app.user != self.context['request'].user:
            raise serializers.ValidationError('You can not create a subscription for an app that you do not own.')

        return Subscription.objects.create(user=self.context['request'].user, **validated_data)
    
    def update(self, instance, validated_data):
        if validated_data.get('app') and instance.app.id != validated_data.get('app'):
            raise serializers.ValidationError('You can not change the app of a subscription.')
            
        return super().update(instance, validated_data)