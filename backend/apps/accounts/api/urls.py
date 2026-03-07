from django.urls import path, include
from rest_framework.routers import SimpleRouter

from apps.accounts.api.views import RegistrationView, BodyMetricsViewSet


router = SimpleRouter()
router.register("body-metrics", BodyMetricsViewSet, basename="body-metrics")

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="bot-register"),
    path("", include(router.urls)),
]
