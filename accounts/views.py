
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render , redirect
from .forms import VerificationCodeForm, PhoneNumberForm
from random import randint
from .utils import send_code
from accounts.models import User


# Create your views here.



def phone_number_view(request):
    if request.method == 'POST':
        form = PhoneNumberForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            name = form.cleaned_data.get('name', '')

            token = str(randint(1000, 9999))
            request.session['phone_number'] = phone_number
            request.session['verification_code'] = token
            request.session['name'] = name

            send_code(phone_number, token)
            return redirect('code_view')
    else:
        form = PhoneNumberForm()

    return render(request, 'registration/login.html', {'form': form})


@login_required
def verify(request):
    if request.method == 'POST':
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data['verification_code']
            stored_code = request.session.get('verification_code')
            phone_number = request.session.get('phone_number')
            name = request.session.get('name')

            if entered_code == stored_code:
                # پیدا کردن یا ساختن کاربر
                user, created = User.objects.get_or_create(phone_number=phone_number)
                user.name = name
                user.save()

                # احراز هویت و لاگین کردن کاربر
                user = authenticate(request, phone_number=phone_number, verification_code=entered_code)
                if user is not None:
                    login(request, user)
                    # پاک کردن داده‌های سشن
                    request.session.pop('verification_code', None)
                    request.session.pop('phone_number', None)
                    request.session.pop('name', None)
                    return redirect('calendar')
                else:
                    form.add_error('verification_code', 'خطا در احراز هویت')
            else:
                form.add_error('verification_code', 'کد وارد شده اشتباه است')
    else:
        form = VerificationCodeForm()

    return render(request, 'registration/verify.html', {'form': form})

@login_required
def welcome(request):
    return render(request, 'registration/welcome.html')

@login_required
def calendar(request):
    return render(request, 'registration/reservation.html')
