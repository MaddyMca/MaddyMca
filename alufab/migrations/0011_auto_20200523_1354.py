# Generated by Django 3.0.6 on 2020-05-23 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0010_auto_20200523_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_working',
            field=models.BooleanField(default=True),
        ),
    ]
