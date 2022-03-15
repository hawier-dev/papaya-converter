from django.urls import path
from .views import dashboard

app_name = "papaya_converter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
]
