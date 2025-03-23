from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/restaurants/', views.restaurants_api, name='restaurants_api'),
    path('api/geocode/', views.geocode_api, name='geocode_api'),
]