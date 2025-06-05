from django import forms

class AppointmentForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    date = forms.DateTimeField(label='Дата и время встречи', widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    purpose = forms.CharField(label='Цель встречи', widget=forms.Textarea, required=False)
