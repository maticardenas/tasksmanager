from django.urls import path
from health import views

urlpatterns = [
    path("liveness/", views.liveness, name="liveness"),
    path("readiness/", views.readiness, name="readiness"),
]
