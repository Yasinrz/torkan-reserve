import jdatetime
from django.contrib.auth.forms import UserChangeForm
from .models import User , SupportTicket ,EmployeeTicket
from home.models import Time
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(label=_('Confirm password'), widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('phone_number', 'name', 'is_superuser',)

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
        fields = ('phone_number', 'name', 'is_superuser',)

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

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get('phone_number')
        name = cleaned_data.get('name')
        if not phone_number:
            raise forms.ValidationError("The phone number cannot be empty.")
        if not phone_number.startswith('09'):
            raise forms.ValidationError("The phone number must start with '09'.")
        if len(phone_number) != 11:
            raise forms.ValidationError("The phone number must be 11 digits long.")
        if not name:
            raise forms.ValidationError("The name cannot be empty.")
        return cleaned_data






    def validate_unique(self):
        """
        Override the unique check so that form doesn't raise error
        if phone_number already exists.
        """
        pass


class VerificationCodeForm(forms.Form):

    verification_code = forms.CharField(max_length=4, required=False ,label='کد اعتبار سنجی' )


class SupportTicketForm(forms.ModelForm):
     class Meta:
        model = SupportTicket
        fields = ('title', 'message' )
        lables ={
            'title': 'موضوع تیکت',
            'message': 'متن پیام',
        }

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'عنوان تیکت'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'پیام خود را بنویسید...'
            }),
        }
        


class EmployeeTicketForm(forms.ModelForm):
    class Meta:
        model = EmployeeTicket
        fields = [
            "employee",
            "ticket_type",
            "leave_start",
            "leave_end",
            "leave_type",
            "facility_amount",
            "facility_duration_months",
            "advance_amount",
            "description",
            "status",
        ]
        labels = {
            "employee": "کارمند",
            "ticket_type": "نوع تیکت",
            "leave_start": "تاریخ شروع مرخصی",
            "leave_end": "تاریخ پایان مرخصی",
            "leave_type": "نوع مرخصی",
            "facility_amount": "مبلغ تسهیلات",
            "facility_duration_months": "مدت بازپرداخت (ماه)",
            "advance_amount": "مبلغ مساعده",
            "description": "توضیحات",
            "status": "وضعیت",
        }
        widgets = {
            "ticket_type": forms.Select(attrs={"class": "form-select"}),
            "leave_start": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "employee": forms.HiddenInput(),
            "ticket_type": forms.Select(attrs={"class": "form-select"}),
            "leave_start": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "leave_end": forms.DateInput(attrs={"type": "date", "class": "form-input"}),
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "facility_amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
            "facility_duration_months": forms.NumberInput(attrs={"class": "form-input"}),
            "advance_amount": forms.NumberInput(attrs={"class": "form-input", "step": "0.01"}),
            "description": forms.Textarea(attrs={"class": "form-textarea", "rows": 4}),
            "status": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        ticket_type = kwargs.pop('ticket_type', None)  # دریافت ticket_type از ویو
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # تنظیم فیلدهای نمایش داده‌شده بر اساس ticket_type
        if ticket_type == 'leave':
            self.fields = {key: self.fields[key] for key in ['employee', 'ticket_type', 'leave_start', 'leave_end', 'leave_type', 'description', 'status']}
        elif ticket_type == 'facility':
            self.fields = {key: self.fields[key] for key in ['employee', 'ticket_type', 'facility_amount', 'facility_duration_months', 'description', 'status']}
        elif ticket_type == 'advance':
            self.fields = {key: self.fields[key] for key in ['employee', 'ticket_type', 'advance_amount', 'description', 'status']}
        elif ticket_type == 'other':
            self.fields = {key: self.fields[key] for key in ['employee', 'ticket_type', 'description', 'status']}

        # تنظیم layout برای Crispy Forms
        self.helper.layout = Layout(
            Field('employee', css_class='hidden'),
            Field('ticket_type', css_class='mb-4'),
            Div(
                Field('leave_start', css_class='mb-4'),
                Field('leave_end', css_class='mb-4'),
                Field('leave_type', css_class='mb-4'),
                css_class='leave-fields' if ticket_type == 'leave' else 'hidden',
            ),
            Div(
                Field('facility_amount', css_class='mb-4'),
                Field('facility_duration_months', css_class='mb-4'),
                css_class='facility-fields' if ticket_type == 'facility' else 'hidden',
            ),
            Div(
                Field('advance_amount', css_class='mb-4'),
                css_class='advance-fields' if ticket_type == 'advance' else 'hidden',
            ),
            Field('description', css_class='mb-4'),
            Field('status', css_class='hidden'),
        )

    def clean(self):
        cleaned_data = super().clean()
        ticket_type = cleaned_data.get("ticket_type")

        # اعتبارسنجی فیلدهای مرتبط با نوع تیکت
        if ticket_type == EmployeeTicket.TicketType.LEAVE:
            if not cleaned_data.get("leave_start") or not cleaned_data.get("leave_end") or not cleaned_data.get("leave_type"):
                raise forms.ValidationError("برای تیکت مرخصی باید تاریخ شروع، پایان و نوع مرخصی را وارد کنید.")
        elif ticket_type == EmployeeTicket.TicketType.FACILITY:
            if not cleaned_data.get("facility_amount"):
                raise forms.ValidationError("برای تیکت تسهیلات باید مبلغ تسهیلات را وارد کنید.")
        elif ticket_type == EmployeeTicket.TicketType.ADVANCE:
            if not cleaned_data.get("advance_amount"):
                raise forms.ValidationError("برای تیکت مساعده باید مبلغ مساعده را وارد کنید.")

        return cleaned_data