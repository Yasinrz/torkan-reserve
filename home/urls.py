from django.urls import path
from . import views
from accounts.views import custom_create_ticket

urlpatterns = [
    path('', views.home, name='home'),
    path('calendar/', views.calendar, name='calendar'),
    path('dashbord/', views.dashbord, name='dashbord'),
    path('contact_us/', lambda request: custom_create_ticket(request, "home/contact_us.html"), name='contact_us'),
]
