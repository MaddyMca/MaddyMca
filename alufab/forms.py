from django import forms
from django.forms import ModelForm
from .models import Employee, measurement,attendance,customer, customer_login, material_inventory,Empattendance



class Calculate_form(forms.ModelForm):
    class Meta:
        model = measurement
        fields = ['customer_name','left','right','top','bottom','track','type','color','mesure_date_time','Payment_per_sqft']
