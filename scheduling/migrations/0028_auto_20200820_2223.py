# Generated by Django 3.0.7 on 2020-08-20 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0027_request_scheduled_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='scheduled_date',
            field=models.DateField(),
        ),
    ]
