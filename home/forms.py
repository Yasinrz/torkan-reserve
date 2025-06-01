from django import forms
from .models import RequestReservation
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
import jdatetime
from django.utils.translation import gettext_lazy as _


class RequestReservationForm(forms.ModelForm):
    class Meta:
        model = RequestReservation
        fields = ('suggested_reservation_date', 'suggested_reservation_time',)
        widgets = {
            'suggested_reservation_time': forms.TimeInput(attrs={'class': 'form-control big-timepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(RequestReservationForm, self).__init__(*args, **kwargs)

        self.fields['suggested_reservation_date'] = JalaliDateField(
            label=_('Requested Data Reservation '),
            widget=AdminJalaliDateWidget
        )
        self.fields['suggested_reservation_date'].widget.attrs.update({'class': 'form-control jalali-date-input'})

    def clean_suggested_reservation_date(self):
        date = self.cleaned_data['suggested_reservation_date']
        gregorian_date = date
        if isinstance(date, jdatetime.date):
            # Convert Jalali date to Gregorian date
            gregorian_date = date.togregorian()
        if gregorian_date < jdatetime.date.today().togregorian():
            raise forms.ValidationError(_("you can't reserve in the past"))
        elif gregorian_date > jdatetime.date.today().togregorian() + jdatetime.timedelta(days=7):
            raise forms.ValidationError(_("you can reserve only for the next 7 days"))
        elif gregorian_date.weekday() == 4:
            raise forms.ValidationError(_("you can't reserve on Friday"))
        return gregorian_date
