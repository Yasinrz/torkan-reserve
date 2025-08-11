from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.phone_number_view, name='login'),
    path('verify/', views.verify, name='code_view'),
    path('welcome/', views.welcome, name='welcome'),
    path('custom_panel/',views.custom_panel, name='custom_panel')

]
