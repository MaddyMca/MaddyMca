# Generated by Django 3.0.4 on 2020-03-26 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='Payment_per_sqft',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='area',
        ),
        migrations.AddField(
            model_name='measurement',
            name='Payment_per_sqft',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='measurement',
            name='total_payment',
            field=models.FloatField(default=0),
        ),
    ]
