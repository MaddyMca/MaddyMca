# Generated by Django 3.0.8 on 2020-07-15 02:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0022_used_material_mat_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='used_material',
            name='userd_on',
            field=models.DateField(default=datetime.datetime.today),
        ),
    ]
