from django.urls import path
from . import views

urlpatterns = [
    #path('', views.home, name='home'),
    path('', views.home, name='home'),
    path('api/reservations/' ,views.reservation_api, name='reservation_api' ),


]