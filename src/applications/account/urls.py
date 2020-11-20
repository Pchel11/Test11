from django.urls import path, include

from applications.account.apps import AccountConfig

app_name = AccountConfig.label

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
]
