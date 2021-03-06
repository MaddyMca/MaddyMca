# Generated by Django 3.0.4 on 2020-03-22 05:55

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(default='Ichalkaranji', max_length=100)),
                ('phono', models.CharField(max_length=10)),
                ('is_complete', models.BooleanField(default=False)),
                ('cust_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('completion_date', models.DateTimeField(null=True)),
                ('area', models.FloatField(default=0)),
                ('Payment_per_sqft', models.FloatField(default=0)),
                ('total_payment', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(default='Ichalkaranji', max_length=100)),
                ('phono', models.CharField(max_length=10)),
                ('designation', models.CharField(choices=[('Manager', 'Manager'), ('Supervisor', 'Supervisor'), ('Admin', 'Admin')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='materialDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_name', models.CharField(max_length=50)),
                ('lowest_limit', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=10)),
                ('Address', models.CharField(max_length=100)),
                ('worker_type', models.CharField(choices=[('glass_cutting', 'Glass_Cutting'), ('fitting', 'fitting'), ('regular', 'regular')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='customer_login',
            fields=[
                ('cust_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='alufab.customer')),
                ('cust_password', models.CharField(max_length=15)),
                ('is_complete', models.BooleanField(default=False)),
                ('cust_review', models.CharField(max_length=100)),
                ('star', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mesure_date_time', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('left', models.FloatField(default=0)),
                ('right', models.FloatField(default=0)),
                ('top', models.FloatField(default=0)),
                ('bottom', models.FloatField(default=0)),
                ('bb', models.FloatField(default=0)),
                ('hi', models.FloatField(default=0)),
                ('g1', models.FloatField(default='0.0')),
                ('g2', models.FloatField(default='0.0')),
                ('color', models.CharField(max_length=20)),
                ('is_complete', models.BooleanField(default=False)),
                ('completion_date', models.DateTimeField(null=True)),
                ('track', models.CharField(choices=[('2T', '2 track'), ('3T', '3 track')], max_length=2)),
                ('type', models.CharField(choices=[('18X35', '18X35'), ('18X50', '18X50')], max_length=6)),
                ('area', models.FloatField(default=0)),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='alufab.customer')),
            ],
        ),
        migrations.CreateModel(
            name='inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material_quantity', models.FloatField(default=0)),
                ('price_per_unit', models.FloatField(default=0)),
                ('total_price', models.FloatField(default=0)),
                ('Purchase_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('material_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='materail', to='alufab.materialDetails')),
            ],
        ),
        migrations.CreateModel(
            name='employeePayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_per_day', models.FloatField(default=0)),
                ('days_present', models.IntegerField(default=0)),
                ('payment', models.FloatField(default=0)),
                ('day_of_payment', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work_in_square_foot', models.FloatField(default=0)),
                ('payment_per_square_ft', models.FloatField(default=0)),
                ('total_payment', models.FloatField(default=0)),
                ('Date_of_attendance', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.customer')),
                ('worker_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.worker')),
            ],
        ),
        migrations.CreateModel(
            name='AbsentEmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Absent_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('cust_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name', to='alufab.Employee')),
            ],
        ),
    ]
