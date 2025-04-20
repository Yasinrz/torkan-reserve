from django import forms
from django.contrib.auth import get_user_model

class PhoneNumberForm(forms.ModelForm):
    class Meta:

        model = get_user_model()
        fields = ['name' , 'phone_number' ]


class VerificationCodeForm(forms.Form):

    verification_code = forms.CharField(max_length=4, required=False ,label='کد اعتبار سنجی' )




