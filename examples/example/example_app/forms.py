from django import forms


class Form(forms.Form):
    name = forms.CharField(max_length=20)
