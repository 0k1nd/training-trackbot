from apps.accounts.api.views import BodyMetricsViewSet, RegistrationView
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register("body-metrics", BodyMetricsViewSet, basename="body-metrics")

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="bot-register"),
    path("", include(router.urls)),
]
