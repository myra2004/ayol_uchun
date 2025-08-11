from django.urls import include, path

app_name = "payments"


urlpatterns = [
    path("paylov/", include("apps.payment.paylov.urls", namespace="paylov")),
]