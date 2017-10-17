from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^service.html$', views.server),
    url(r'^test.html$', views.test),
]
