from django import forms

class NameForm(forms.Form):
    your_name = forms.CharField(label='name', max_length=100)
