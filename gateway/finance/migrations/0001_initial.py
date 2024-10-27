# Generated by Django 4.2 on 2024-10-27 22:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GateWay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gatway_url_request', models.CharField(blank=True, max_length=150, null=True, verbose_name='gateway url request')),
                ('gateway_verify_url', models.CharField(blank=True, max_length=150, null=True, verbose_name='gateway urlverification')),
                ('gateway_code', models.BigIntegerField(choices=[('parsian', 'parsian'), ('saman', 'saman'), ('shaparak', 'shaparak'), ('zarin', 'zarin')], max_length=20, verbose_name='gateway code')),
                ('is_enable', models.BooleanField(default=True, verbose_name='is enabled')),
                ('auth_data', models.CharField(blank=True, null=True, verbose_name='data authentication')),
            ],
            options={
                'verbose_name': 'Gateway',
                'verbose_name_plural': 'Gateways',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='invoice number')),
                ('amount', models.PositiveIntegerField(verbose_name='payment amount')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
                ('payment_log', models.TextField(blank=True, verbose_name='payment log')),
                ('authority', models.CharField(blank=True, max_length=64, verbose_name='authority')),
                ('gateway', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='finance.gateway', verbose_name='payments')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Payment',
                'verbose_name_plural': 'Payments',
            },
        ),
    ]
