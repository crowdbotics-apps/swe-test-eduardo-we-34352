from rest_framework import mixins, viewsets

from apps.applications.api.v1.serializers import PlanSerializer
from apps.applications.models import Plan

class PlanViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
