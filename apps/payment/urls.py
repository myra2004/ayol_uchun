from django.urls import include, path

from apps.payment.views import (
    OrderCreateAPIView,
    AddUserCardAPIView,
    ConfirmUserCardAPIView,
)

app_name = "payment"


urlpatterns = [
    path("order/create/", OrderCreateAPIView.as_view(), name="create-order"),
    path("usercard/add/", AddUserCardAPIView.as_view(), name="add-usercard"),
    path("usercard/confirm/", ConfirmUserCardAPIView.as_view(), name="confirm-usercard"),

    # Payment Provider callbacks
    path("paylov/", include("apps.payment.paylov.urls", namespace="paylov")),
]