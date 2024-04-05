# Generated by Django 5.0 on 2024-04-03 07:57

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CarCompany', '0005_alter_carreservation_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carreservation',
            name='car_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CarCompany.car'),
        ),
        migrations.AlterField(
            model_name='carreservation',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 3, 7, 59, 8, 677155, tzinfo=datetime.timezone.utc)),
        ),
    ]
