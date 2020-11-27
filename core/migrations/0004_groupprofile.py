# Generated by Django 3.0.7 on 2020-07-04 18:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('scheduling', '0017_auto_20200701_2207'),
        ('core', '0003_auto_20200701_2205'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.Group')),
                ('name', models.CharField(max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.Company')),
            ],
        ),
    ]