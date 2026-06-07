from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

# Registration Form for new users
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')
    first_name = forms.CharField(max_length=50, required=True, label='First Name')
    last_name = forms.CharField(max_length=50, required=True, label='Last Name')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email


# Form for updating User model attributes (first_name, last_name, email)
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


# Form for updating Profile model attributes (address, city, state, postal code, etc.)
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Street Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State / Province'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Zip / Postal Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
