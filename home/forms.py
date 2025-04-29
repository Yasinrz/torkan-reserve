from django import forms
from .models import RequestReservation

class RequestReservationForm(forms.ModelForm):
    class Meta:
        model = RequestReservation
        fields = ('suggested_reservation_date',)
        widgets = {
            'suggested_reservation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
