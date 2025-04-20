from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import VerificationCodeForm, PhoneNumberForm
from random import randint
from .utils import send_code
from .models import Time
from accounts.models import User
import jdatetime


def home(request):
    return render(request, 'home/home.html')


def welcome(request):
    return render(request, 'home/welcome.html')


def phone_number_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            name = form.cleaned_data.get('name', '')  # Get name if available

            # Generate a random 4-digit session code
            token = str(randint(1000, 9999))
            request.session['phone_number'] = phone_number
            request.session['verification_code'] = token
            request.session['name'] = name

            send_code(phone_number, token)

            return redirect('code_view')

    else:
        form = PhoneNumberForm()

        return render(request, 'home/register.html', {'form': form})


def verify(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            stored_code = request.session.get('verification_code')
            phone_number = request.session.get('phone_number')
            name = request.session.get('name')

            if entered_code == stored_code:

                user, created = User.objects.get_or_create(phone_number=phone_number)
                user.name = name
                user.save()

                # Clear session data
                request.session.pop('verification_code', None)
                request.session.pop('phone_number', None)
                request.session.pop('name', None)

                return redirect('calendar')
            else:
                form.add_error('verification_code', 'کد وارد شده اشتباه است')
    else:
        form = VerificationCodeForm()

    return render(request, 'home/verify.html', {'verify_form': form})


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


def calendar(request):
    return render(request, 'home/reservation.html')
