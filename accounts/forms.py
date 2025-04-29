import jdatetime
from django.contrib.auth.forms import UserChangeForm
from .models import User
from home.models import Time
from django import forms
from django.contrib.auth import get_user_model


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'is_superuser', 'is_staff',)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        is_superuser = cleaned_data.get("is_superuser")
        if is_superuser:
            if not password1:
                raise forms.ValidationError("رمز عبور برای مدیر (superuser) الزامی است.")
            if password1 != password2:
                raise forms.ValidationError("رمز عبور و تکرار آن یکسان نیستند.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password1 = forms.CharField(label='Password1', widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'is_superuser', 'is_staff',)

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password1 = self.cleaned_data.get('password1')
        if password1:
            user.set_password(password1)
        if commit:
            user.save()
            self.save_m2m()
        return user


class PhoneNumberForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['name', 'phone_number']



class VerificationCodeForm(forms.Form):

    verification_code = forms.CharField(max_length=4, required=False ,label='کد اعتبار سنجی' )


