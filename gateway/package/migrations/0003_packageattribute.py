# Generated by Django 4.2 on 2024-11-08 23:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0002_package_is_enable'),
    ]

    operations = [
        migrations.CreateModel(
            name='PackageAttribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attributes', to='package.package')),
            ],
        ),
    ]
