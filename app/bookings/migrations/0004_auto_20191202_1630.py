# Generated by Django 3.0 on 2019-12-02 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_auto_20191202_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookings',
            name='date',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
