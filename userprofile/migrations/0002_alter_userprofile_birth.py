# Generated by Django 5.1.5 on 2025-02-08 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]
