from django.urls import path

from web import views

urlpatterns = [
    path('', views.main, name="main"),
    path('start_service', views.start_service, name="start_service"),
]
