from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'city', 'state', 'postal_code', 'country']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            
        # Customize placeholder labels
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['address'].widget.attrs['placeholder'] = 'Street Address'
        self.fields['city'].widget.attrs['placeholder'] = 'City'
        self.fields['state'].widget.attrs['placeholder'] = 'State / Province'
        self.fields['postal_code'].widget.attrs['placeholder'] = 'Zip / Postal Code'
        self.fields['country'].widget.attrs['placeholder'] = 'Country'
