from django.urls import path
from . import views


urlpatterns = [
    path('package/', views.package),
]
