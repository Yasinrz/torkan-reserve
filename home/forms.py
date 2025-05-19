from django import forms
from .models import RequestReservation
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
import jdatetime
from django.utils.translation import gettext_lazy as _


class RequestReservationForm(forms.ModelForm):
    class Meta:
        model = RequestReservation
        fields = ('suggested_reservation_date', 'suggested_reservation_time', )
        widgets = {
            'suggested_reservation_time': forms.TimeInput(attrs={'class': 'form-control big-timepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(RequestReservationForm, self).__init__(*args, **kwargs)

        self.fields['suggested_reservation_date'] = JalaliDateField(
            label=_('Requested Data Reservation '),
            widget=AdminJalaliDateWidget
        )
        self.fields['suggested_reservation_date'].widget.attrs.update({'class': 'data-jdp-only-date'})

    def clean_suggested_reservation_date(self):
        data = self.cleaned_data['suggested_reservation_date']
        if isinstance(data, jdatetime.date):
            # Convert Jalali date to Gregorian date
            return data.togregorian()
        return data
