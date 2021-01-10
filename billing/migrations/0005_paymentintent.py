# Generated by Django 3.0.7 on 2021-01-10 20:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0045_auto_20210103_2109'),
        ('billing', '0004_auto_20210110_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentIntent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_id', models.CharField(max_length=255, null=True, unique=True)),
                ('client_secret', models.CharField(max_length=255, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('application_fee_amount', models.FloatField(default=0)),
                ('amount', models.FloatField(default=0)),
                ('amount_received', models.FloatField(default=0)),
                ('request', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheduling.Request')),
            ],
        ),
    ]
