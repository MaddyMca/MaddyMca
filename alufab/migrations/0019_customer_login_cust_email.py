# Generated by Django 3.0.6 on 2020-06-11 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0018_customer_login_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer_login',
            name='cust_email',
            field=models.CharField(default='modern@gmail.com', max_length=100),
            preserve_default=False,
        ),
    ]
