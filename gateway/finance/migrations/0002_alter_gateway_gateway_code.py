# Generated by Django 4.2 on 2024-10-27 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='gateway_code',
            field=models.BigIntegerField(choices=[('parsian', 'parsian'), ('saman', 'saman'), ('shaparak', 'shaparak'), ('zarin', 'zarin')], verbose_name='gateway code'),
        ),
    ]
