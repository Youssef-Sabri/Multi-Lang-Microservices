from django.urls import path
from .views import summarize, get_status

urlpatterns = [
    path("summarize", summarize, name="summarize"),
    path("summarize/status/<str:id>", get_status, name="get_status"),
]
