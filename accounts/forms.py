from django import forms
from .models import User


class RegistrationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Your Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number. Ex: 010..'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password', ]

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']

        if password != confirm_password:
            print('Password and confirm password does not match!')
            raise forms.ValidationError('Password and confirm password does not match!')
