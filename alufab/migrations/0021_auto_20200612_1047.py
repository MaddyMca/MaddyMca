# Generated by Django 3.0.6 on 2020-06-12 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0020_auto_20200612_0954'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='material_inventory',
            name='used',
        ),
        migrations.CreateModel(
            name='Used_material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used', models.FloatField(default=0)),
                ('Emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.Employee')),
                ('cust_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alufab.customer')),
            ],
        ),
    ]
