from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse


# from datetime import DateField, date, timezone

# Create your models here.
class Employee(models.Model):
    Emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    phono = models.IntegerField(default=0)
    Address = models.CharField(default=' ',max_length=100)
    city = models.CharField(default='Ichalkaranji',max_length=20)
    de = [
        ('Manager','Manager'),
        ('Supervisor','Supervisor'),
        ('Admin', 'Admin')
    ]
    designation = models.CharField(max_length=10, choices=de)
    Paymentperday = models.FloatField(default=0)
    is_working=models.BooleanField(default=True)
    def __int__(self):

        return self.Emp_id

class customer(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100,default='Ichalkaranji')
    phono = models.CharField(max_length=10)
    is_complete = models.BooleanField(default=False)
    cust_date = models.DateField(default=datetime.now, blank=True)
    completion_date = models.DateField(null=True)
    total_payment = models.FloatField(default=0)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('update_customer',kwargs={'id':self.pk})



class measurement(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    mesure_date_time = models.DateField(default=datetime.now, blank=True)
    customer_name = models.ForeignKey(customer, on_delete=models.CASCADE)
    left = models.FloatField(default=0)
    right = models.FloatField(default=0)
    top = models.FloatField(default=0)
    bottom = models.FloatField(default=0)
    bb = models.FloatField(default=0)
    hi = models.FloatField(default=0)
    g1 = models.FloatField(default='0.0')
    g2 = models.FloatField(default='0.0')
    color = models.CharField(max_length=20)
    is_complete = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    completion_date = models.DateField(null=True)
    Payment_per_sqft = models.FloatField(default=0)
    total_payment = models.FloatField(default=0)

    TRACK = [
        ('2T', '2 track'),
        ('3T', '3 track')
    ]
    TY = [
        ('18X35', '18X35'),
        ('18X50', '18X50')
    ]
    track = models.CharField(max_length=2, choices=TRACK)
    type = models.CharField(max_length=6, choices=TY)
    area = models.FloatField(default=0)
    cost = models.FloatField(default=0)
    def __int__(self):
        return self.customer_name

class worker(models.Model):
    worker_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=10)
    Address = models.CharField(max_length=100)

    WT = [
        ('glass_cutting', 'Glass_Cutting'),
        ('fitting', 'fitting'),
        ('regular', 'regular')
    ]
    worker_type = models.CharField(max_length=100, choices=WT)

    def __str__(self):
        return self.worker_name


class attendance(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    worker_name = models.ForeignKey(worker, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(customer, on_delete=models.CASCADE)
    work_in_square_foot = models.FloatField(default=0)
    payment_per_square_ft = models.FloatField(default=0)
    total_payment = models.FloatField(default=0)
    Date_of_attendance = models.DateField(default=datetime.now, blank=True)

    def __int__(self):
        return self.emp_id


class material_inventory(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    material_name=models.CharField(max_length=20)
    matrial_description=models.CharField(max_length=100)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)
    total_amt = models.FloatField(default=0)
    is_user = models.BooleanField(default=False)

class Used_material(models.Model):
    used = models.FloatField(default=0)
    cust_name=models.ForeignKey(customer, on_delete=models.CASCADE)
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
class Empattendance(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    Attend = models.BooleanField(default=False)

class emp_pay(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now, blank=True)
    attent = models.IntegerField(default=0)
    Payment = models.FloatField(default=0)

class bill(models.Model):
    Emp_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    customer_name = models.ForeignKey(customer, on_delete=models.CASCADE)
    completion_date = models.DateField(null=True)
    total_payment = models.FloatField(default=0)
    paid_payment = models.FloatField(default=0)
    payment_date = models.DateField(null=True)





class customer_login(models.Model):
    cust_name = models.OneToOneField(customer,on_delete = models.CASCADE, primary_key = True)
    cust_email = models.CharField(max_length=100)
    cust_password = models.CharField(max_length = 15)
    is_complete = models.BooleanField(default = False)
    cust_review = models.CharField(max_length = 100)
    star = models.IntegerField(default = 0)
    otp = models.IntegerField(default=0)
