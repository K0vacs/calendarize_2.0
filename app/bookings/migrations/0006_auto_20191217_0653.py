# Generated by Django 3.0 on 2019-12-17 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_auto_20191213_0648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='date',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
