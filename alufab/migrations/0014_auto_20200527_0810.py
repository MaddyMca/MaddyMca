# Generated by Django 3.0.6 on 2020-05-27 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0013_auto_20200527_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='PAymentperday',
            field=models.FloatField(default=0),
        ),
    ]
