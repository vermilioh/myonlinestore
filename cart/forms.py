from django import forms


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    delivery_method = forms.CharField(max_length=255)
    payment_method = forms.CharField(max_length=255)
