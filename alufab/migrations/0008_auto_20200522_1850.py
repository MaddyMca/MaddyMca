# Generated by Django 3.0.6 on 2020-05-22 18:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0007_auto_20200522_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='customer',
        ),
        migrations.AddField(
            model_name='customer',
            name='Emp_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='leaves',
            field=models.IntegerField(default=15),
        ),
        migrations.AddField(
            model_name='material_inventory',
            name='Emp_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='Emp_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='emp_pay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.datetime.now)),
                ('attent', models.FloatField(default=0)),
                ('Payment', models.FloatField(default=0)),
                ('Emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee')),
            ],
        ),
        migrations.CreateModel(
            name='bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateField(null=True)),
                ('total_payment', models.FloatField(default=0)),
                ('paid_payment', models.FloatField(default=0)),
                ('payment_date', models.DateField(null=True)),
                ('Emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee')),
                ('customer_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.customer')),
            ],
        ),
    ]
