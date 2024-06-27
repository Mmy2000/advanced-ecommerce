from django import forms
from .models import  Profile 
from accounts.models import User
from django.utils.translation import gettext_lazy as _


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Enter Password'),
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': _('Confirm Password')
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = _('Enter First Name')
        self.fields['last_name'].widget.attrs['placeholder'] = _('Enter last Name')
        self.fields['phone_number'].widget.attrs['placeholder'] = _('Enter Phone Number')
        self.fields['email'].widget.attrs['placeholder'] = _('Enter Email Address')
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['address','image','country','city','company','headline','about','address_line_1','address_line_2']