# Generated by Django 3.0.7 on 2020-07-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0019_auto_20200723_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='about',
            field=models.CharField(default='', max_length=2550),
        ),
    ]
