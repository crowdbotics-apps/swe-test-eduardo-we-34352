from rest_framework import mixins, viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from apps.applications.api.v1.permissions import IsOwner
from apps.applications.api.v1.serializers import AppSerializer, PlanSerializer, SubscriptionSerializer
from apps.applications.models import App, Plan, Subscription

class DefaultAuthConfViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    class Meta:
        abstract = True

class PlanViewSet(viewsets.ReadOnlyModelViewSet, DefaultAuthConfViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer

class AppViewSet(viewsets.ModelViewSet, DefaultAuthConfViewSet):
    permissions_classes = [IsAuthenticated, IsOwner]
    queryset = App.objects.all()
    serializer_class = AppSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

class SubscriptionViewSet(DefaultAuthConfViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permissions_classes = [IsAuthenticated, IsOwner]
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    