from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.phone_number_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path('employee_login/', views.employee_login, name='employee_login'),
    path('profile/', views.staff_or_customer, name='profile'),
    path('verify/', views.verify, name='code_view'),
    path('welcome/', views.welcome, name='welcome'),
    path('custom_panel/',views.custom_panel, name='custom_panel'),
    path('ticket_success/',views.ticket_success, name='ticket_success' ),
    path('custom_ticket/',views.custom_create_ticket, name='custom_ticket'),
    path('staff_create_ticket/',views.staff_create_ticket,name='staff_ticket'),
    path('employee_panel/',views.employee_panel, name='employee_panel'),
    path('answer_custom/', views.answer_custom, name='answer_custom'),
    path('answer_employee/', views.answer_employee , name='answer_employee'),
    path('suggestion/', views.suggestion , name='suggestion'),
]
