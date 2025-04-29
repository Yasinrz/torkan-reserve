
from django.shortcuts import render
from django.http import JsonResponse
from .models import Time
import jdatetime


def home(request):
    return render(request, 'home/home.html')


def reservation_api(request):
    reservations = Time.objects.all()
    events = [
        {
            'title': 'رزرو شده',
            'start': jdatetime.date.fromgregorian(date=res.shamsi_date).isoformat(),
            'color': 'red'
        }
        for res in reservations
    ]
    return JsonResponse(events, safe=False)


