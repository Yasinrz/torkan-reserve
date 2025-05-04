from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Time
from .forms import RequestReservationForm
import jdatetime
from .utils import send_temporary



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

            phone = reservation.user.phone_number
            name = reservation.user.name
            miladi_date = form.cleaned_data['suggested_reservation_date']
            date = jdatetime.date.fromgregorian(date=miladi_date)

            send_temporary(phone, name, date)
            return redirect('welcome')
    else:
        form = RequestReservationForm()

    return render(request, 'home/reservation.html', {'form': form})

