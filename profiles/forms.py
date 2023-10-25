from django import forms
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=15)
    country = forms.CharField(max_length=200)
    usdt_wallet = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Set placeholders for each field
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['usdt_wallet'].widget.attrs['placeholder'] = 'USDT TRC20 Wallet Address (for payment)'
        self.fields['country'].widget.attrs['placeholder'] = 'Country'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Phone Number'

        # Hide labels
        for field in self.fields.values():
            field.label = ''
    
    class Meta:
        model = UserProfile
        exclude = ['user','username', 'email', 'referrer', 'referral_code', 'email_verified']


class CreateUserForm(UserCreationForm):
    username = forms.CharField(max_length=200)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        # Set placeholders for each field
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        # self.fields['usdt_wallet'].widget.attrs['placeholder'] = 'USDT TRC20 Wallet Address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'

        # Hide labels
        for field in self.fields.values():
            field.label = ''

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('Email already exists!')
        return self.cleaned_data['email']

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
        }

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        # Hide labels for username and password fields
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        for field in self.fields.values():
            field.label = ''