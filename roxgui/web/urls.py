from django.urls import path

from web import views

urlpatterns = [
    path('', views.main, name="web_main"),
    path("start_service", views.start_service, name="web_start_service"),
    path("stop_service", views.stop_service, name="web_stop_service"),
]
