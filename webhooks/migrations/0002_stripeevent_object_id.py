# Generated by Django 3.0.7 on 2020-08-26 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webhooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stripeevent',
            name='object_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
