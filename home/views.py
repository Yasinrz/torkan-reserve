from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Time
from .forms import RequestReservationForm
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


@login_required
def calendar(request):
    if request.method == 'POST':
        form = RequestReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            return redirect('home')
    else:
        form = RequestReservationForm()
    return render(request, 'home/reservation.html', {'form': form})
