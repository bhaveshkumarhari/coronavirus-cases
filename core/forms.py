from django import forms

class ContactForm(forms.Form):
    country1 = forms.CharField()
    country2 = forms.CharField()