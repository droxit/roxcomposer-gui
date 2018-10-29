from django.urls import path

from web import views

urlpatterns = [
    path('', views.web_main, name="web_main"),
]
