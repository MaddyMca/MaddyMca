# Generated by Django 3.0.8 on 2020-07-15 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alufab', '0021_auto_20200612_1047'),
    ]

    operations = [
        migrations.AddField(
            model_name='used_material',
            name='Mat_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='alufab.material_inventory'),
            preserve_default=False,
        ),
    ]