# Generated by Django 3.0.6 on 2020-06-06 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0016_measurement_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_pay',
            name='attent',
            field=models.IntegerField(default=0),
        ),
    ]
