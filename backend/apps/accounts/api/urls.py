from django.urls import path
from apps.accounts.api.views import RegistrationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="bot-register"),
]
