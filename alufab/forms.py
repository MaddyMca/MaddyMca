from django import forms
from django.forms import ModelForm
from .models import Employee, measurement,attendance,customer, customer_login


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['designation']

class Calculate_form(forms.ModelForm):
    class Meta:
        model = measurement
        fields = ['customer_name','left','right','top','bottom','track','type','color','mesure_date_time','Payment_per_sqft']

class Attend_form(forms.ModelForm):
    class Meta:
        model= attendance
        fields = ['worker_name','customer_name']
