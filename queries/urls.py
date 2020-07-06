from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='query'),
    path('proxy/<str:phrase>', views.proxy, name='proxy'),
]