from django import forms
from . models import User ,Time
# from django_jalali.forms import JalaliDateWidget
from django_jalali.admin.widgets import AdminjDateWidget

class PhoneNumberForm(forms.ModelForm):
    class Meta:

        model = User
        fields = ['name' , 'phone_number' ]


class VerificationCodeForm(forms.Form):

    verification_code = forms.CharField(max_length=4, required=False ,label='کد اعتبار سنجی' )




