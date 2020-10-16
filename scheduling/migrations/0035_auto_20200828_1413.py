# Generated by Django 3.0.7 on 2020-08-28 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0034_auto_20200826_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='private',
        ),
        migrations.AddField(
            model_name='company',
            name='_is_viewable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='_stripe_charges_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='_stripe_default_currency',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='_stripe_details_submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='_stripe_payouts_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='config',
            name='allow_card_payment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='config',
            name='allow_unpaid_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='config',
            name='private',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='config',
            name='show_employees',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='config',
            name='show_services',
            field=models.BooleanField(default=True),
        ),
    ]
