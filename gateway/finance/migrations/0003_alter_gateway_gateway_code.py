# Generated by Django 4.2 on 2024-11-09 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_alter_gateway_gateway_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='gateway_code',
            field=models.CharField(choices=[('parsian', 'parsian'), ('saman', 'saman'), ('shaparak', 'shaparak'), ('zarin', 'zarin')], max_length=150, verbose_name='gateway code'),
        ),
    ]