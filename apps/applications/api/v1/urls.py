from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.applications.api.v1 import viewsets

router = DefaultRouter()
router.register("plan", viewsets.PlanViewSet, basename="plan")
router.register("app", viewsets.AppViewSet, basename="app")
router.register("subscription", viewsets.SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path("", include(router.urls)),
]
