from django.urls import include, path

from apps.payment.views import (
    OrderCreateAPIView,
)

app_name = "payments"


urlpatterns = [
    path("order/create/", OrderCreateAPIView.as_view(), name="create-order"),

    # Payment Provider callbacks
    path("paylov/", include("apps.payment.paylov.urls", namespace="paylov")),
]