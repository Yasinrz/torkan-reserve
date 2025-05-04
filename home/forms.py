
from django import forms
from .models import RequestReservation
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django_jalali.admin.widgets import AdminjDateWidget
from django_jalali.forms import jDateField
import jdatetime


class RequestReservationForm(forms.ModelForm):
    # suggested_reservation_date = jDateField(widget=AdminjDateWidget)
    class Meta:
        model = RequestReservation
        fields = ('suggested_reservation_date',)

    def __init__(self, *args, **kwargs):
        super(RequestReservationForm, self).__init__(*args, **kwargs)

        self.fields['suggested_reservation_date'] = JalaliDateField(
            label='تقویم',
            widget=AdminJalaliDateWidget
        )
        self.fields['suggested_reservation_date'].widget.attrs.update({'class': 'data-jdp-only-date'})

    def clean_suggested_reservation_date(self):
        data = self.cleaned_data['suggested_reservation_date']
        if isinstance(data, jdatetime.date):
            # Convert Jalali date to Gregorian date
            return data.togregorian()
        return data
