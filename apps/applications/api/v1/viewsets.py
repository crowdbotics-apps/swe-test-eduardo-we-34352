from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from apps.applications.api.v1.permissions import IsOwner

from apps.applications.api.v1.serializers import AppSerializer, PlanSerializer
from apps.applications.models import App, Plan

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
        return super().get_queryset().filter(created_by=self.request.user)